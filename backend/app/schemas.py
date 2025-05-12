from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

from datetime import datetime
from pydantic import BaseModel

class TaskCreate(BaseModel):
    content: str

class TaskResponse(BaseModel):
    id: UUID
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserResponse(UserBase):
    id: UUID
    message: str

    class Config:
        from_attributes  = True

class ReactionCreate(BaseModel):
    task_id: UUID
    reaction_type: str

class ReactionResponse(BaseModel):
    id: UUID
    task_id: UUID
    user_id: UUID
    reaction_type: str

    class Config:
        orm_mode = True

