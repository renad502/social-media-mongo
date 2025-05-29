from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.follow_schema import FollowResponse
from app.api.deps import get_current_active_user
from app.services.follow_service import follow_user, unfollow_user, get_followers, get_following

router = APIRouter(prefix="/follow", tags=["follow"])

@router.post("/{username}")
async def follow(username: str, current_user=Depends(get_current_active_user)):
    success = await follow_user(current_user["_id"], username)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already following or user does not exist")
    return {"detail": f"You are now following {username}"}

@router.delete("/{username}")
async def unfollow(username: str, current_user=Depends(get_current_active_user)):
    success = await unfollow_user(current_user["_id"], username)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not following or user does not exist")
    return {"detail": f"You have unfollowed {username}"}

@router.get("/followers/{username}", response_model=List[FollowResponse])
async def list_followers(username: str):
    followers = await get_followers(username)
    return followers

@router.get("/following/{username}", response_model=List[FollowResponse])
async def list_following(username: str):
    following = await get_following(username)
    return following
