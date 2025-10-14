from pydantic import BaseModel, Field
from typing import Optional


class IssueTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class IssueTypeCreate(IssueTypeBase):
    pass


class IssueTypeResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
