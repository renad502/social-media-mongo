from pydantic import BaseModel, Field
from datetime import datetime
from app.db.models.user_model import PyObjectId

class Follow(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    follower_id: PyObjectId
    followee_id: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {str: str}
