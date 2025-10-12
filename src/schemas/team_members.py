from pydantic import BaseModel, Field
from typing import Optional

class TeamMemberCreate(BaseModel):
    user_id: int = Field(..., description="User ID to add to team")

class TeamMemberResponse(BaseModel):
    id: int
    team_id: int
    user_id: int

    class Config:
        from_attributes = True

class TeamMemberWithUser(BaseModel):
    id: int
    team_id: int
    user_id: int
    name: str
    email: str

    class Config:
        from_attributes = True
