from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


from typing import Optional
from datetime import datetime

class BaseOrganizationSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)

class OrganizationCreate(BaseOrganizationSchema):
    pass

class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)

class OrganizationResponse(BaseOrganizationSchema):
    id: int
    name:str
    created_at: datetime
    updated_at: datetime
