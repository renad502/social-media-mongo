from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class DirectMessageBase(BaseModel):
    content: str
    media_url: Optional[str] = None

class DirectMessageCreate(DirectMessageBase):
    recipient_username: str

class DirectMessageInDB(DirectMessageBase):
    id: str = Field(..., alias="_id")
    sender_id: str
    recipient_id: str
    created_at: datetime

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat(),
        }
