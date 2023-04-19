import os
from jose import jwt
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from dotenv import load_dotenv
from urllib.parse import quote_plus
from fastapi.middleware.cors import CORSMiddleware

from models import PersonalDevelopmentArea, UserModel
from schemas import User


# Load environment variables from .env file
load_dotenv()


# Get database details from environment variables
DB_NAME = os.environ.get("DB_NAME")
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = quote_plus(os.environ.get("DB_PASSWORD"))
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")



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
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# OAuth2 authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# login endpoint
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    # Generate access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username, "role": db_user.role},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "role":db_user.role}



# create user endpoint
@app.post("/users")
def create_user(user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password
    db_user = UserModel(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/personalDevelopmentAreas")
def create_text(content: str, db: Session = Depends(get_db)):
    text = PersonalDevelopmentArea(content=content)
    db.add(text)
    db.commit()
    db.refresh(text)
    return text


@router.get("/personalDevelopmentAreas")
def read_all_text(db: Session = Depends(get_db)):
    texts = db.query(PersonalDevelopmentArea).all()
    if not texts:
        raise HTTPException(status_code=404, detail="No Data found")
    return texts


@router.get("/personalDevelopmentAreas/{id}")
def read_text(id: int, db: Session = Depends(get_db)):
    text = db.query(PersonalDevelopmentArea).filter(PersonalDevelopmentArea.id == id).first()
    if not text:
        raise HTTPException(status_code=404, detail="Data not found")
    return text


@router.put("/personalDevelopmentAreas/{id}")
def update_text(id: int, content: str, db: Session = Depends(get_db)):
    text = db.query(PersonalDevelopmentArea).filter(PersonalDevelopmentArea.id == id).first()
    if not text:
        raise HTTPException(status_code=404, detail="Data not found")
    text.content = content
    db.commit()
    db.refresh(text)
    return text


@router.delete("/personalDevelopmentAreas/{id}")
def delete_text(id: int, db: Session = Depends(get_db)):
    text = db.query(PersonalDevelopmentArea).filter(PersonalDevelopmentArea.id == id).first()
    if not text:
        raise HTTPException(status_code=404, detail="Data not found")
    db.delete(text)
    db.commit()
    return {"message": "Data deleted"}


app.include_router(router)

