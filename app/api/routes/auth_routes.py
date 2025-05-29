from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import authenticate_user, create_access_token
from app.schemas.user_schema import Token, UserLogin, UserCreate
from datetime import timedelta, datetime
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.db.database import db
from app.core.security import get_password_hash
from app.enums.user_enums import UserRole

auth_router = APIRouter(tags=["auth"])  # single router with tag

@auth_router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["email"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    if user.role not in UserRole:
        raise HTTPException(status_code=400, detail="Role must be either 'admin' or 'user'")

    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user.password)
    user_dict["created_at"] = datetime.utcnow()
    user_dict["is_active"] = True

    result = await db.users.insert_one(user_dict)
    return {"id": str(result.inserted_id), "username": user.username, "email": user.email, "role": user.role.value}
