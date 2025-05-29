from bson import ObjectId
from app.db.database import db
from datetime import datetime
from app.db.models.comment_model import comment_helper

async def create_comment(post_id: str, user_id: str, content: str):
    comment = {
        "post_id": ObjectId(post_id),
        "author_id": ObjectId(user_id),
        "content": content,
        "created_at": datetime.utcnow()
    }
    result = await db.comments.insert_one(comment)
    created = await db.comments.find_one({"_id": result.inserted_id})
    return comment_helper(created)

async def get_comments_by_post(post_id: str):
    comments = []
    async for comment in db.comments.find({"post_id": ObjectId(post_id)}):
        comments.append(comment_helper(comment))
    return comments

async def update_comment(comment_id: str, user_id: str, content: str):
    comment = await db.comments.find_one({"_id": ObjectId(comment_id)})
    if not comment:
        return None
    if str(comment["author_id"]) != user_id:
        return "unauthorized"
    await db.comments.update_one({"_id": ObjectId(comment_id)}, {"$set": {"content": content}})
    updated = await db.comments.find_one({"_id": ObjectId(comment_id)})
    return comment_helper(updated)

async def delete_comment(comment_id: str, user_id: str):
    comment = await db.comments.find_one({"_id": ObjectId(comment_id)})
    if not comment:
        return None
    if str(comment["author_id"]) != user_id:
        return "unauthorized"
    await db.comments.delete_one({"_id": ObjectId(comment_id)})
    return True
