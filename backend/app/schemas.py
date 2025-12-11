from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class UserBase(BaseModel):
    name: str
    email: str
    role: str
    department: str
    date_joined: date

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    users: List[User]
    total: int
    page: int
    limit: int
    total_pages: int