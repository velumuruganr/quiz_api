from sqlalchemy import Column, Integer, String, Enum as EnumColumn
from enum import Enum
from sqlalchemy.ext.declarative import declarative_base

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
    

class PersonalDevelopmentArea(Base):
    __tablename__ = "personal_development_areas"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255))
    
    
class School(Base):
    __tablename__ = "schools"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    sentence = Column(String(255), index=True)