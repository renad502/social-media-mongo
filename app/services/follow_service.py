from app.db.database import db
from app.db.models.user_model import PyObjectId
from typing import List

async def follow_user(follower_id: str, followee_username: str) -> bool:
    followee = await db.users.find_one({"username": followee_username})
    if not followee:
        return False
    # Check if already following
    existing = await db.follows.find_one({
        "follower_id": PyObjectId(follower_id),
        "followee_id": followee["_id"]
    })
    if existing:
        return False
    follow_doc = {
        "follower_id": PyObjectId(follower_id),
        "followee_id": followee["_id"]
    }
    await db.follows.insert_one(follow_doc)
    return True

async def unfollow_user(follower_id: str, followee_username: str) -> bool:
    followee = await db.users.find_one({"username": followee_username})
    if not followee:
        return False
    result = await db.follows.delete_one({
        "follower_id": PyObjectId(follower_id),
        "followee_id": followee["_id"]
    })
    return result.deleted_count > 0

async def get_followers(username: str) -> List[dict]:
    user = await db.users.find_one({"username": username})
    if not user:
        return []
    pipeline = [
        {"$match": {"followee_id": user["_id"]}},
        {"$lookup": {
            "from": "users",
            "localField": "follower_id",
            "foreignField": "_id",
            "as": "follower"
        }},
        {"$unwind": "$follower"},
        {"$project": {
            "username": "$follower.username",
            "bio": "$follower.bio",
            "avatar_url": "$follower.avatar_url"
        }}
    ]
    cursor = db.follows.aggregate(pipeline)
    return [doc async for doc in cursor]

async def get_following(username: str) -> List[dict]:
    user = await db.users.find_one({"username": username})
    if not user:
        return []
    pipeline = [
        {"$match": {"follower_id": user["_id"]}},
        {"$lookup": {
            "from": "users",
            "localField": "followee_id",
            "foreignField": "_id",
            "as": "followee"
        }},
        {"$unwind": "$followee"},
        {"$project": {
            "username": "$followee.username",
            "bio": "$followee.bio",
            "avatar_url": "$followee.avatar_url"
        }}
    ]
    cursor = db.follows.aggregate(pipeline)
    return [doc async for doc in cursor]
