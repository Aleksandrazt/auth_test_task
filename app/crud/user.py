"""
Пользователи
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User as user_model
from app.core.security import PasswordCoder

# Если будут еще модели тут обопщить 
# и вынести взяти по id и прочее в абстрактный круд


class User:
    """
    Взаимодействие с пользователями
    """
    # тут не обвязательно но потенциально так удобнее будет обопщать
    model = user_model

    async def get_user_by_email(self, db: AsyncSession, email: str):
        """
        Найти пользователя по email
        """
        quary = await db.execute(select(self.model).where(self.model.email == email))
        return quary.scalar_one_or_none()

    async def get_user_by_id(self, db: AsyncSession, user_id: int):
        """
        Получить пользователя по id
        """
        quary = await db.execute(select(self.model).where(self.model.id == user_id))
        return quary.scalar_one_or_none()

    async def create_user(self, db: AsyncSession, email: str, password: str):
        """
        Создать пользователя
        """
        hashed_password = PasswordCoder().get_password_hash(password)
        user = self.model(email=email, hashed_password=hashed_password)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
