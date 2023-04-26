from sqlalchemy import Column, ForeignKey, Integer, String, Enum as EnumColumn, DateTime
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
    name = Column(String(255))
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
    

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    mobile_number = Column(String, unique=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    school = relationship("School", back_populates="teachers")
    user = relationship("User", back_populates="teacher")
