from app.db.database import db
from app.db.models.user_model import PyObjectId
from typing import Optional

async def get_user_by_username(username: str) -> Optional[dict]:
    return await db.users.find_one({"username": username})

async def get_user_by_id(user_id: str) -> Optional[dict]:
    return await db.users.find_one({"_id": PyObjectId(user_id)})

async def update_user_profile(user_id: str, bio: Optional[str], avatar_url: Optional[str]) -> bool:
    update_data = {}
    if bio is not None:
        update_data["bio"] = bio
    if avatar_url is not None:
        update_data["avatar_url"] = avatar_url
    if not update_data:
        return False
    result = await db.users.update_one({"_id": PyObjectId(user_id)}, {"$set": update_data})
    return result.modified_count > 0
