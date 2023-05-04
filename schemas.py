from typing import List, Optional
from pydantic import BaseModel
from models import UserRole

# Pydantic model for creating a new user
class UserRequest(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole
    
# create a Pydantic model for the request body to create a new school
class SchoolCreate(BaseModel):
    name: str
    address: str

# create a Pydantic model for the request body to update an existing school
class SchoolUpdate(BaseModel):
    name: Optional[str]
    address: Optional[str]

    # define a method to iterate over the fields of the model
    def __iter__(self):
        for field in self.__fields__:
            value = getattr(self, field)
            if value is not None:
                yield field, value

# create a Pydantic model for the response body representing a school
class SchoolResponse(BaseModel):
    id: int
    name: str
    address: str

    class Config:
        orm_mode = True
        

class JWTUser(BaseModel):
    sub : str
    role : UserRole
    

class PasswordUpdateRequest(BaseModel):
    token : str
    old_password : str
    new_password : str
    
    
class TeacherCreate(BaseModel):
    school_name: str
    username: str
    email: str
    password: str
    confirm_password: str

class Teacher(BaseModel):
    id: int
    school_id: int
    user_id: int

    class Config:
        orm_mode = True


class TeacherDetails(BaseModel):
    id:int
    username: str
    email: str
    school_name: str
    school_address: str
    
    
# Schemas for Test

class TestQuestionChoiceCreate(BaseModel):
    choice_text: str
    is_correct: bool


class TestQuestionChoiceUpdate(BaseModel):
    id: int
    choice_text: str
    is_correct: bool


class TestQuestionCreate(BaseModel):
    question_text: str
    choices: List[TestQuestionChoiceCreate]


class TestQuestionUpdate(BaseModel):
    id: int
    question_text: str
    choices: List[TestQuestionChoiceUpdate]
    new_choices: Optional[List[TestQuestionChoiceCreate]]
    deleted_choices: Optional[List[int]]


class TestCreate(BaseModel):
    name: str
    school_id : int
    questions: List[TestQuestionCreate]


class TestUpdate(BaseModel):
    id: int
    name: str
    questions: List[TestQuestionUpdate]
    new_questions: Optional[List[TestQuestionCreate]]
    deleted_questions: Optional[List[int]]

    
    
class TestQuestionChoice(BaseModel):
    id: int
    choice_text: str
    is_correct: bool

    class Config:
        orm_mode = True


class TestQuestion(BaseModel):
    id: int
    question_text: str
    choices: List[TestQuestionChoice]

    class Config:
        orm_mode = True


class Test(BaseModel):
    id: int
    name: str
    questions: List[TestQuestion]

    class Config:
        orm_mode = True


# Schemas for Test Result

class TestResultCreate(BaseModel):
    test_id: int
    student_id: int
    answers: List[int]


# class TestResult(BaseModel):
#     id: int
#     test: Test
#     student: User
#     answers: List[int]
#     score: float

#     class Config:
#         orm_mode = True
            
class Profile(BaseModel):
    username:str
    email: str

class ForgetPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password:str