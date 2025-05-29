from app.db.database import db
from app.db.models.post_model import PostModel
from bson import ObjectId
from datetime import datetime


async def create_post(author_id: str, data: dict):
    post = PostModel(author_id=ObjectId(author_id), **data)
    await db.posts.insert_one(post.dict(by_alias=True))
    return post


async def get_post(post_id: str):
    post = await db.posts.find_one({"_id": ObjectId(post_id)})
    return post


async def update_post(post_id: str, data: dict):
    data["updated_at"] = datetime.utcnow()
    await db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": data})
    return await get_post(post_id)


async def delete_post(post_id: str):
    result = await db.posts.delete_one({"_id": ObjectId(post_id)})
    return result.deleted_count
