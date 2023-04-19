from pydantic import BaseModel
from models import UserRole

# Pydantic model for creating a new user
class UserRequest(BaseModel):
    username: str
    email: str
    name: str
    password: str
    role: UserRole
    
# create a Pydantic model for the request body to create a new school
class SchoolCreate(BaseModel):
    name: str
    address: str

# create a Pydantic model for the request body to update an existing school
class SchoolUpdate(BaseModel):
    name: str = None
    address: str = None

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