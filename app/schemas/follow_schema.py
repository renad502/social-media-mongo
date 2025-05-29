from pydantic import BaseModel
from datetime import datetime
class FollowCreate(BaseModel):
    followee_username: str  # username of the user to follow



class FollowResponse(BaseModel):
    follower_id: str
    following_id: str
    followed_at: datetime

    class Config:
        from_attributes = True 