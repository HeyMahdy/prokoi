from fastapi import APIRouter, HTTPException, Request, status, Depends, Query
from fastapi.security import HTTPBearer
from src.services.labels import LabelsService
from src.schemas.labels import LabelCreate, LabelUpdate, LabelResponse, IssueLabelAssignment, IssueLabelResponse
from typing import List
from src.notification.streams import  acknowledge_notifications
from src.schemas.notification import AcknowledgeRequest



router = APIRouter(prefix="/api/notifications", tags=["Notifications"])




@router.post("/ACKNOWLEDGE")
async def acknowledge_notification(req: AcknowledgeRequest):
    print(req.user_id, req.message_ids)
    
    await acknowledge_notifications(req.user_id, req.message_ids)
    return {"message":"seen"}