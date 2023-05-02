import os
from jose import jwt
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, subqueryload
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from dotenv import load_dotenv
from urllib.parse import quote_plus
from fastapi.middleware.cors import CORSMiddleware
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import secrets
import datetime
from models import PersonalDevelopmentArea, School, Teacher, User
from schemas import JWTUser, PasswordUpdateRequest, SchoolCreate, SchoolResponse, SchoolUpdate, TeacherDetails, UserRequest
import schemas
import models
import uvicorn

# Load environment variables from .env file
load_dotenv()

BASE_URL = os.environ.get("BASE_URL")

# Get database details from environment variables
DB_NAME = os.environ.get("DB_NAME")
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = quote_plus(os.environ.get("DB_PASSWORD"))
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")

SMTP_EMAIL = os.environ.get("SMTP_EMAIL")
SMTP_PASSWORD = quote_plus(os.environ.get("SMTP_PASSWORD"))

# JWT configuration
SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# initializing the FastAPI
app = FastAPI()
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# database configuration
DATABASE_URL = f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# Dependency to get a database session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# helper functions for password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


# Create access token
def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# OAuth2 authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_username(token: str):
    # Verify the JWT token and extract the email address
    try:
        jwt_user = JWTUser(**jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]))
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Return the user details
    return jwt_user

# login endpoint
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == form_data.username).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    # Generate access token
    access_token = create_access_token(
        data={"sub": db_user.username, "role": db_user.role},
    )
    return {"access_token": access_token, "token_type": "bearer", "role":db_user.role}


@app.put("/update_password")
async def update_password(request: PasswordUpdateRequest, db: Session = Depends(get_db)):

    
    username = get_username(request.token)
    user = db.query(User).filter(User.username == username.sub).first()
    # Check if the email address is valid
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify the old password
    if not pwd_context.verify(request.old_password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    # Hash the new password
    hashed_password = pwd_context.hash(request.new_password)
    
    # Update the user's password
    user.password = hashed_password
    
    db.commit()
    db.refresh(user)
    
    return {"message": "Password updated successfully"}


# Generate token
def generate_token(length=32):
    return secrets.token_hex(length)


# Update user token
def update_user_token(user_id: int, token: str, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.password_reset_token = token
    user.password_reset_token_created_at = datetime.datetime.utcnow()
    db.commit()


# Check if token is valid
def is_token_valid(user: models.User, token: str) -> bool:
    if not user.password_reset_token or not user.password_reset_token_created_at:
        return False

    elapsed_time = datetime.datetime.utcnow() - user.password_reset_token_created_at
    if elapsed_time > datetime.timedelta(minutes=60):
        return False

    return user.password_reset_token == token

@app.post("/reset-password")
def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.password_reset_token == request.reset_token).first()
    if db_user is None or not is_token_valid(db_user, request.reset_token):
        raise HTTPException(status_code=404, detail="Invalid Token")
    hashed_password = get_password_hash(request.new_password)
    db_user.password = hashed_password
    db_user.password_reset_token = None
    db_user.password_reset_token_created_at = None
    db.add(db_user)
    db.commit()
    return {"message": "Password updated successfully"}

@app.post('/forget-password')
def forget_password(request: schemas.ForgetPasswordRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == request.email).first()
        # Check if the email address is valid
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    # Generate a unique token for the user
    token = generate_token()

    # Update user database with token and token expiry time
    update_user_token(db_user.id, token, db)

    # Create email message
    msg = MIMEMultipart()
    msg['From'] = "One Decision Quiz"
    msg['To'] = request.email
    msg['Subject'] = 'Reset Password'

    # Create HTML message
    html = f"<p>Hi {db_user.username},</p>"
    html += "<p>You have requested to reset your password. Please click on the link below to reset your password:</p>"
    html += f"<a href='{BASE_URL}updatePassword/{token}'>{BASE_URL}updatePassword/{token}</a>"
    html += "<p>This link will expire in one hour.</p>"
    msg.attach(MIMEText(html, 'html'))

    # Connect to SMTP server and send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, request.email, msg.as_string())
        server.quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email Error:{e}")

    return {"message": "Reset password email sent"}

# create user endpoint
@app.post("/users")
def create_user(user: UserRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Create a new teacher
@router.post("/teachers")
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    if teacher.password != teacher.confirm_password:
        raise HTTPException(status_code=404, detail="Password and Confirm Password not Matching")
    hashed_password = get_password_hash(teacher.password)
    db_user = db.query(User).filter(User.username == teacher.username).first()
    if db_user is not None:
        raise HTTPException(status_code=404, detail="Username already Exists")
    db_user = models.User(
        email=teacher.email,
        username=teacher.username,
        password=hashed_password,
        role="teacher"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    school = db.query(School).filter(School.name == teacher.school_name).first()
    db_teacher = models.Teacher(
        user_id=db_user.id,
        school_id=school.id
    )
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    
    return TeacherDetails(
        id=db_teacher.id,
        username=db_user.username,
        email=db_user.email,
        school_name=school.name,
        school_address=school.address,
        )


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# def update_user(user_id: int, user: schemas.UserRequest, db: Session = Depends(get_db)):
#     db_teacher = db.query(User).filter(User.id == user_id).first()
#     if not db_teacher:
#         raise HTTPException(status_code=404, detail="User not found")
#     for attr, value in user.dict(exclude_unset=True).items():
#         setattr(db_teacher, attr, value)
#     db.commit()
#     db.refresh(db_teacher)
#     return db_teacher


# Get a teacher by ID
@router.get("/teachers/{teacher_id}")
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    user = db.query(User).filter(User.id == db_teacher.user_id).first()
    school = db.query(School).filter(School.id == db_teacher.school_id).first()
    return TeacherDetails(
        id=db_teacher.id,
        username=user.username,
        email=user.email,
        school_name=school.name,
        school_address=school.address,
        )


@router.get("/profile")
def get_profile(token:str, db: Session = Depends(get_db)):
    username = get_username(token)
    user = db.query(User).filter(User.username == username.sub).first()
    if user:
        return {
            "username":user.username,
            "email":user.email,
        }

# Get all teachers
@router.get("/teachers")
def read_teachers(db: Session = Depends(get_db)):
    teachers = db.query(Teacher).join(User).join(School).all()
    all_teachers = []
    for db_teacher in teachers:
        user = db.query(User).filter(User.id == db_teacher.user_id).first()
        school = db.query(School).filter(School.id == db_teacher.school_id).first()
        all_teachers.append(TeacherDetails(
            id=db_teacher.id,
            username=user.username,
            email=user.email,
            school_name=school.name,
            school_address=school.address,
            )) 
    return all_teachers


# Update a teacher by ID
@router.put("/teachers/{teacher_id}")
def update_teacher(teacher_id: int, teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not db_teacher:
        return None
    update_data = teacher.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_teacher, key, value)
    db_user = get_user_by_id(db, db_teacher.user_id)
    if db_user:
        db_user.email = teacher.email
        db_user.username = teacher.username
        db.commit()
    db.commit()
    db.refresh(db_teacher)
    return {"message":"Teacher Updated Successfully"}


# Delete a teacher by ID
@router.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not db_teacher:
        return None
    # Delete associated user
    db_user = get_user_by_id(db, db_teacher.user_id)
    if db_user:
        db.delete(db_user)
    db.delete(db_teacher)
    db.commit()
    return {'message': 'Teacher Deleted'}


#CRUD API for Personal Development Areas

# create a new area
@router.post("/personalDevelopmentAreas")
def create_area(content: str, db: Session = Depends(get_db)):
    text = PersonalDevelopmentArea(content=content)
    db.add(text)
    db.commit()
    db.refresh(text)
    return text

# get all areas
@router.get("/personalDevelopmentAreas")
def read_all_areas(db: Session = Depends(get_db)):
    texts = db.query(PersonalDevelopmentArea).all()
    if not texts:
        raise HTTPException(status_code=404, detail="No Data found")
    return texts

# get a specific area by ID
@router.get("/personalDevelopmentAreas/{id}")
def read_area(id: int, db: Session = Depends(get_db)):
    text = db.query(PersonalDevelopmentArea).filter(PersonalDevelopmentArea.id == id).first()
    if not text:
        raise HTTPException(status_code=404, detail="Data not found")
    return text

# update a specific area by ID
@router.put("/personalDevelopmentAreas/{id}")
def update_area(id: int, content: str, db: Session = Depends(get_db)):
    text = db.query(PersonalDevelopmentArea).filter(PersonalDevelopmentArea.id == id).first()
    if not text:
        raise HTTPException(status_code=404, detail="Data not found")
    text.content = content
    db.commit()
    db.refresh(text)
    return text

# delete a specific area by ID
@router.delete("/personalDevelopmentAreas/{id}")
def delete_area(id: int, db: Session = Depends(get_db)):
    text = db.query(PersonalDevelopmentArea).filter(PersonalDevelopmentArea.id == id).first()
    if not text:
        raise HTTPException(status_code=404, detail="Data not found")
    db.delete(text)
    db.commit()
    return {"message": "Data deleted"}


#CRUD API for Schools

# create a new school
@router.post("/schools", response_model=SchoolResponse)
def create_school(school: SchoolCreate, db: Session = Depends(get_db)):
    new_school = School(**school.dict())
    db.add(new_school)
    db.commit()
    db.refresh(new_school)
    return new_school

# get all schools
@router.get("/schools", response_model=List[SchoolResponse])
def read_all_schools(db: Session = Depends(get_db)):
    schools = db.query(School).all()
    return schools

# get a specific school by ID
@router.get("/schools/{school_id}", response_model=SchoolResponse)
def read_school(school_id: int, db: Session = Depends(get_db)):
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school

# update a specific school by ID
@router.put("/schools/{school_id}", response_model=SchoolResponse)
def update_school(school_id: int, school: SchoolUpdate, db: Session = Depends(get_db)):
    existing_school = db.query(School).filter(School.id == school_id).first()
    if not existing_school:
        raise HTTPException(status_code=404, detail="School not found")
    for field, value in school:
        setattr(existing_school, field, value)
    db.commit()
    return existing_school

# delete a specific school by ID
@router.delete("/schools/{school_id}")
def delete_school(school_id: int, db: Session = Depends(get_db)):
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    db.delete(school)
    db.commit()
    return {"message": "School deleted successfully"}


#CRUD for tests

#create a new test

@router.post("/tests/", response_model=schemas.Test)
def create_test(test: schemas.TestCreate, db: Session = Depends(get_db)):
    db_test = models.Test(name=test.name, teacher_id=test.teacher_id)
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    for question in test.questions:
        db_question = models.Question(question_text=question.question_text, test_id=db_test.id)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        for choice in question.choices:
            db_choice = models.Choice(text=choice.text,is_correct=choice.is_correct, question_id=db_question.id)
            db.add(db_choice)
            db.commit()
            db.refresh(db_choice)
    return db_test


@router.get("/tests/", response_model=List[schemas.Test])
def read_tests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tests = db.query(models.Test).offset(skip).limit(limit).all()
    return tests


@router.get("/tests/{test_id}", response_model=schemas.TestDetail)
def read_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(models.Test).filter(models.Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not found")
    return test


@router.put("/tests/{test_id}", response_model=schemas.Test)
def update_test(test_id: int, test: schemas.TestUpdate, db: Session = Depends(get_db)):
    db_test = db.query(models.Test).filter(models.Test.id == test_id).first()
    if not db_test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not found")
    db_test.title = test.title
    db_test.description = test.description
    db_test.duration = test.duration
    db_test.start_time = test.start_time
    db_test.end_time = test.end_time
    db.commit()
    db.refresh(db_test)
    return db_test


@router.delete("/tests/{test_id}")
def delete_test(test_id: int, db: Session = Depends(get_db)):
    db_test = db.query(models.Test).filter(models.Test.id == test_id).first()
    if not db_test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not found")
    db.delete(db_test)
    db.commit()
    return {"detail": "Test deleted"}@app.route('/test', methods=['POST'])

app.include_router(router)

def main():
    uvicorn.run(app, port=8000)
    
if __name__ == "__main__":
    main()