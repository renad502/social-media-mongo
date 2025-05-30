from fastapi import APIRouter, Depends, HTTPException
from app.schemas.post_schema import PostCreate, PostUpdate, PostResponse
from app.services.post_service import create_post, get_post, update_post, delete_post
from app.api.deps import get_current_user
from bson import ObjectId
from app.services.onesignal_service import send_notification_via_onesignal
from app.db.database import db
from datetime import datetime, timezone

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostResponse, status_code=201)
async def create_new_post(post: PostCreate, current_user: dict = Depends(get_current_user)):
    # Assuming you're actually creating a post here, not a comment:
    new_post = {
        "title": post.title,
        "content": post.content,
        "user_id": current_user["_id"],
        "username":current_user["username"],
        "created_at": datetime.now(timezone.utc),
    }
    result = await db["posts"].insert_one(new_post)
    new_post["_id"] = result.inserted_id
    return PostResponse(**new_post, id=str(new_post["_id"]), author_id=str(new_post["user_id"]))


@router.get("/{post_id}", response_model=PostResponse)
async def read_post(post_id: str):
    post = await get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostResponse(**post, id=str(post["_id"]), author_id=str(post["author_id"]))


@router.put("/{post_id}", response_model=PostResponse)
async def edit_post(post_id: str, data: PostUpdate, current_user: dict = Depends(get_current_user)):
    post = await get_post(post_id)
    if not post or str(post["author_id"]) != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized to edit this post")
    updated_post = await update_post(post_id, data.dict(exclude_unset=True))
    return PostResponse(**updated_post, id=str(updated_post["_id"]), author_id=str(updated_post["author_id"]))


@router.delete("/{post_id}", status_code=204)
async def remove_post(post_id: str, current_user: dict = Depends(get_current_user)):
    post = await get_post(post_id)
    if not post or str(post["author_id"]) != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    await delete_post(post_id)
    return
