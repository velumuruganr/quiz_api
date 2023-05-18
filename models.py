from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum as EnumColumn, DateTime, Table
from enum import Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()
    
    
test_schools = Table('test_schools', Base.metadata,
    Column('test_id', Integer, ForeignKey('tests.id')),
    Column('school_id', Integer, ForeignKey('schools.id'))
)


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
    questions = relationship("Question", back_populates="pda")


class School(Base):
    __tablename__ = "schools"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    
    teachers = relationship("Teacher", back_populates="school")
    students = relationship("Student", back_populates="school")
    tests = relationship('Test',secondary=test_schools, back_populates='schools')


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

    questions = relationship("Question", back_populates="test")
    results = relationship("Result", back_populates="test")

    schools = relationship('School',secondary=test_schools, back_populates='tests')
    
    
class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    pda_id = Column(Integer, ForeignKey("personal_development_areas.id"), nullable=False)
    question_text = Column(String)
    
    test_id = Column(Integer, ForeignKey("tests.id"))
    
    pda = relationship("PersonalDevelopmentArea", back_populates="questions")
    choices = relationship("Choice", back_populates="question")
    test = relationship("Test", back_populates="questions")
    
    
class Choice(Base):
    __tablename__ = "choices"

    id = Column(Integer, primary_key=True, index=True)
    choice_text = Column(String)
    is_correct = Column(Boolean, default=False)
    
    question_id = Column(Integer, ForeignKey("questions.id"))
    
    question = relationship("Question", back_populates="choices")

    
class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    total_questions = Column(Integer)
    correctly_answered = Column(Integer)
    created_at = Column(DateTime)

    
    test_id = Column(Integer, ForeignKey("tests.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    
    test = relationship("Test", back_populates="results")
    student = relationship("Student", back_populates="results")
    

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    class_group = Column(String(255))
    school_id = Column(Integer, ForeignKey("schools.id"))
    
    
    school = relationship("School", back_populates="students")
    results = relationship("Result", back_populates="student")