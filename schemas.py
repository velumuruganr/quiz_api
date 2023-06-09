from typing import List, Optional
from pydantic import BaseModel
from models import UserRole
from datetime import datetime

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
class School(BaseModel):
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
    

class PersonalDevelopmentArea(BaseModel):
    id: int
    content: str
    
    class Config:
        orm_mode = True
    
# Schemas for Test

class TestQuestionChoiceCreate(BaseModel):
    choice_text: str
    is_correct: bool


class TestQuestionChoiceUpdate(BaseModel):
    id: int | None
    choice_text: str
    is_correct: bool


class TestQuestionCreate(BaseModel):
    question_text: str
    pda_id: int
    choices: List[TestQuestionChoiceCreate]


class TestQuestionUpdate(BaseModel):
    id: int | None
    question_text: str
    pda_id: int | None
    pda: PersonalDevelopmentArea | None
    choices: List[TestQuestionChoiceUpdate]


class TestCreate(BaseModel):
    name: str
    school_ids: List[int]
    questions: List[TestQuestionCreate]


class TestUpdate(BaseModel):
    id: int | None
    name: str
    school_ids: List[int]
    questions: List[TestQuestionUpdate]

    
    
class TestQuestionChoice(BaseModel):
    id: int
    choice_text: str
    is_correct: bool

    class Config:
        orm_mode = True


        
        
class TestQuestion(BaseModel):
    id: int
    question_text: str
    pda: PersonalDevelopmentArea
    choices: List[TestQuestionChoice]

    class Config:
        orm_mode = True




class Test(BaseModel):
    id: int
    name: str
    schools: List[School]
    questions: List[TestQuestion]

    class Config:
        orm_mode = True

            
class Profile(BaseModel):
    username:str
    email: str

class ForgetPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password:str
    
    
# create a Pydantic model for the request body to create a new school
class StudentCreate(BaseModel):
    name: str
    year_group: str
    school_id: int


# create a Pydantic model for the request body to update an existing student
class StudentUpdate(BaseModel):
    name: Optional[str]
    year_group: Optional[str]
    school_id: int
    # define a method to iterate over the fields of the model
    def __iter__(self):
        for field in self.__fields__:
            value = getattr(self, field)
            if value is not None:
                yield field, value


# create a Pydantic model for the response body representing a student
class Student(BaseModel):
    id: int
    name: str
    year_group: str
    registered_at: datetime
    school: School

    class Config:
        orm_mode = True
        

class ResultAnswerCreate(BaseModel):
    question_id: int
    selected_choices: List[int]


# create a Pydantic model for the request body to create a new school
class ResultCreate(BaseModel):
    test_id: int
    student_id: int
    answers: List[ResultAnswerCreate]

# class ResultAnswers(BaseModel):
#     question_id: int
#     is_correct: bool


class Answer(BaseModel):
    id:int
    total_choices: int
    correctly_answered: int
    mark: float
    question: TestQuestion

    class Config:
        orm_mode = True

# create a Pydantic model for the response body representing a student
class Result(BaseModel):
    id: int
    created_at: datetime
    total_questions: int
    correctly_answered: int
    answers: List[Answer]
    student: Student
    test: Test
    # answers: List[ResultAnswers]

    class Config:
        orm_mode = True

class TestsPerMonth(BaseModel):
    year: int
    month: int
    test_count: int

    class Config:
        orm_mode = True