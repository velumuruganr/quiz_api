from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum as EnumColumn, DateTime
from enum import Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

# user roles enum
class UserRole(str, Enum):
    admin = "admin"
    teacher = "teacher"


# user model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    role = Column(EnumColumn(UserRole))
    password_reset_token = Column(String(35))
    password_reset_token_created_at = Column(DateTime)
    
    teacher = relationship("Teacher", back_populates="user")

class PersonalDevelopmentArea(Base):
    __tablename__ = "personal_development_areas"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255))
    
    
class School(Base):
    __tablename__ = "schools"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    address = Column(String(255), index=True)
    
    teachers = relationship("Teacher", back_populates="school")
    tests = relationship("Test", back_populates="school")

    

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    school = relationship("School", back_populates="teachers")
    user = relationship("User", back_populates="teacher")


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)

    questions = relationship("Question", back_populates="test")
    school = relationship("School",back_populates="tests")
    
class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String)
    
    test_id = Column(Integer, ForeignKey("tests.id"))
    
    choices = relationship("Choice", back_populates="question")
    answers = relationship("Answer", back_populates="question")
    test = relationship("Test", back_populates="questions")
    
class Choice(Base):
    __tablename__ = "choices"

    id = Column(Integer, primary_key=True, index=True)
    choice_text = Column(String)
    is_correct = Column(Boolean, default=False)
    
    question_id = Column(Integer, ForeignKey("questions.id"))
    
    question = relationship("Question", back_populates="choices")
    
class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("questions.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    question = relationship("Question", back_populates="answers")
    student = relationship("Student", back_populates="answers")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    answers = relationship("Answer", back_populates="student")