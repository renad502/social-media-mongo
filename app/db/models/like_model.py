from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

class LikeModel(BaseModel):
    user_id: str = Field(..., example="user_id")
    post_id: str = Field(..., example="post_id")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "60f7a9d8b8b8b8b8b8b8b8b8",
                "post_id": "60f7a9d8b8b8b8b8b8b8b8b9"
            }
        }
