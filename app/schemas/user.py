"""
Описание представления пользователя
"""

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    """
    Создание пользователя
    """

    email: EmailStr
    password: str


class UserRead(BaseModel):
    """
    Чтение пользователя
    """

    id: int
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True) 
