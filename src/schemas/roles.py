

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime



class permission (BaseModel):

    name: str

class roleOut (BaseModel):
    name: str
    permissions: list[permission]


