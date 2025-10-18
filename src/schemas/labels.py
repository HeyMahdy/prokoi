from pydantic import BaseModel, Field
from typing import Optional


class LabelBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    color: Optional[str] = Field(None, max_length=7, description="Hex color code")


class LabelCreate(LabelBase):
    pass


class LabelUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    color: Optional[str] = Field(None, max_length=7, description="Hex color code")


class LabelResponse(BaseModel):
    id: int
    project_id: int
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class IssueLabelAssignment(BaseModel):
    label_id: int = Field(..., gt=0)


class IssueLabelResponse(BaseModel):
    issue_id: int
    label_id: int
    label_name: str
    label_color: Optional[str] = None

    class Config:
        from_attributes = True
