from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status
from app.db.database import db

async def send_message(sender_id: ObjectId, recipient_username: str, content: str, media_url: str | None):
    recipient = await db.users.find_one({"username": recipient_username})
    if not recipient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipient not found")

    doc = {
        "sender_id": sender_id,
        "recipient_id": recipient["_id"],
        "content": content,
        "media_url": media_url,
        "created_at": datetime.utcnow(),
    }

    result = await db.direct_messages.insert_one(doc)
    return str(result.inserted_id)
