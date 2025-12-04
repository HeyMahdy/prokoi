from pydantic import BaseModel, Field 
from typing import Optional, List, Dict 


class NotificationRedirection(BaseModel):
    type: str
    url: str
    open_in_new_tab: Optional[bool]

class NotificationAction(BaseModel):
    label: str
    action: str
    color_code: str
    url: Optional[str]
    data: str

class NotificationRequestData(BaseModel):
    user_id: str

    message: str

from pydantic import BaseModel
from typing import List


class NotificationResponse(BaseModel):
    message_id: str


class AcknowledgeRequest(BaseModel):
    user_id: int
    message_ids: List[str]


class AcknowledgeResponse(BaseModel):
    success: bool = True
