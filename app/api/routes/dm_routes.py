from fastapi import APIRouter, Depends, status
from bson import ObjectId
from app.schemas.dm_schema import DirectMessageCreate
from app.services.dm_service import send_message
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/dm", tags=["Direct Messages"])

@router.post("/{username}", status_code=status.HTTP_201_CREATED)
async def send_direct_message(
    username: str,
    message: DirectMessageCreate,
    current_user: dict = Depends(get_current_active_user)
):
    message_id = await send_message(
        sender_id=current_user["_id"],
        recipient_username=username,
        content=message.content,
        media_url=message.media_url,
    )
    return {"message_id": message_id, "status": "Message sent"}
