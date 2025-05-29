from app.db.database import db
from bson import ObjectId
from fastapi import HTTPException, status

async def like_post(user_id: str, post_id: str):
    existing = await db.likes.find_one({"user_id": user_id, "post_id": post_id})
    if existing:
        raise HTTPException(status_code=400, detail="Already liked this post.")
    
    await db.likes.insert_one({
        "user_id": user_id,
        "post_id": post_id
    })
    return {"message": "Post liked"}

async def unlike_post(user_id: str, post_id: str):
    result = await db.likes.delete_one({"user_id": user_id, "post_id": post_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Like not found")
    return {"message": "Post unliked"}
