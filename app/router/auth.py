"""
Авторизация
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import PasswordCoder, create_access_token
from app.core.user import get_current_user, get_session, get_settings
from app.crud.user import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserRead)
async def signup(payload: UserCreate, db: AsyncSession = Depends(get_session)):
    """
    Регистрация
    """
    user_crud = User()
    exists = await user_crud.get_user_by_email(db, payload.email)
    if exists:
        raise HTTPException(status_code=400, detail="Данная почта уже занята")
    user = await user_crud.create_user(db, payload.email, payload.password)
    return user


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
    settings=Depends(get_settings),
):
    """
    Вход
    """
    user_crud = User()
    user = await user_crud.get_user_by_email(db, form_data.username)
    if not user or not PasswordCoder().verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = create_access_token(
        subject=str(user.id),
        secret_key=settings.JWT_SECRET,
        expire_minutes=settings.JWT_EXPIRE_MINUTES
    )
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
async def me(current_user=Depends(get_current_user)):
    """
    Страница пользователя
    """
    return current_user
