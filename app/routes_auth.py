# register an dlogin routes for users
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User as UserModel
from app.schemas import UserCreate, UserLogin, Token, User as UserSchema
from app.auth import create_access_token, get_password_hash, verify_password
from app.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserSchema)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(UserModel).filter(UserModel.email == user.email))
    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = UserModel(email=user.email, password=get_password_hash(user.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(UserModel).filter(UserModel.email == form_data.username))
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
