"""
Реализация шифрования и токенов
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext


class PasswordCoder:
    """
    Кодировшик
    """

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password: str) -> str:
        """
        Преобразовать пароль к хэшу
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Сравнение пароля и хешом
        """
        return self.pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, secret_key: str, expire_minutes: int) -> str:
    """
    Получить jwt тоекн
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(expire_minutes))
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, secret_key, algorithm="HS256")


def decode_access_token(token: str, secret_key: str):
    """
    Проверить jwt токен
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except JWTError:
        return None
