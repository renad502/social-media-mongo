from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.comment_schema import CommentCreate, CommentResponse, CommentUpdate
from app.services.comments_service import (create_comment, get_comments_by_post, update_comment, delete_comment
)
from app.api.deps import get_current_user
from bson.errors import InvalidId

router = APIRouter(tags=["Comments"])

@router.post("/posts/{post_id}/comments", response_model=CommentResponse)
async def post_comment(post_id: str, comment: CommentCreate, user: dict = Depends(get_current_user)):
    try:
        return await create_comment(post_id, user["id"], comment.content)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid post ID")

@router.get("/posts/{post_id}/comments", response_model=list[CommentResponse])
async def list_comments(post_id: str):
    try:
        return await get_comments_by_post(post_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid post ID")

@router.put("/comments/{comment_id}", response_model=CommentResponse)
async def edit_comment(comment_id: str, comment: CommentUpdate, user: dict = Depends(get_current_user)):
    result = await update_comment(comment_id, user["id"], comment.content)
    if result is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if result == "unauthorized":
        raise HTTPException(status_code=403, detail="Not allowed to edit this comment")
    return result

@router.delete("/comments/{comment_id}")
async def remove_comment(comment_id: str, user: dict = Depends(get_current_user)):
    result = await delete_comment(comment_id, user["id"])
    if result is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if result == "unauthorized":
        raise HTTPException(status_code=403, detail="Not allowed to delete this comment")
    return {"detail": "Comment deleted"}
