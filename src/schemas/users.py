
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class BaseUserSchema(BaseModel):
    name:str = Field(..., min_length=1)
    email:str = Field(..., min_length=1)

class UserSchema(BaseUserSchema):
    password_hash: str= Field(..., min_length=1)

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(BaseUserSchema):
    id: int
    last_login_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str
