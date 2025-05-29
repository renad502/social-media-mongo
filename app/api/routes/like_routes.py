from fastapi import APIRouter, Depends, HTTPException
from app.schemas.like_schema import LikeResponse
from app.services.like_service import like_post, unlike_post
from app.api.deps import get_current_user
from app.services.onesignal_service import send_notification_via_onesignal
router = APIRouter(tags=["Likes"])
from bson import ObjectId
from app.db.database import db

@router.post("/{post_id}/", response_model=LikeResponse)
async def like_post(post_id: str, current_user: dict = Depends(get_current_user)):
   return await like_post(current_user["_id"], post_id)
  
@router.delete("/posts/{post_id}/like", response_model=LikeResponse)
async def unlike(post_id: str, current_user: dict = Depends(get_current_user)):
    return await unlike_post(current_user["_id"], post_id)
