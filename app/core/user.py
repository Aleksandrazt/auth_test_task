"""
Определение пользователя
"""

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.crud.user import User as user_crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_session(request: Request):
    """
    Получение сессии
    """
    async_sessionmaker = request.app.state.async_sessionmaker
    async with async_sessionmaker() as session:
        yield session


def get_settings(request: Request):
    """
    Получение настроек
    """
    return request.app.state.settings


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
    request: Request = None,
):
    """
    Получить текущего пользователя
    """
    settings = request.app.state.settings
    payload = decode_access_token(token, settings.JWT_SECRET)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный токен"
        )
    user_id = int(payload.get("sub"))
    user = await user_crud().get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return user
