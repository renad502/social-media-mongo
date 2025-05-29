from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user_schema import UserResponse, UserUpdate
from app.api.deps import get_current_active_user
from app.services.user_service import get_user_by_username, update_user_profile

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{username}", response_model=UserResponse)
async def read_user_profile(username: str):
    user = await get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/me", response_model=UserResponse)
async def update_profile(user_update: UserUpdate, current_user=Depends(get_current_active_user)):
    success = await update_user_profile(current_user["_id"], user_update.bio, user_update.avatar_url)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No changes detected")
    updated_user = await get_user_by_username(current_user["username"])
    return updated_user
