from pydantic import BaseModel
from models import UserRole

# Pydantic model for creating a new user
class User(BaseModel):
    username: str
    email: str
    name: str
    role: UserRole
    
