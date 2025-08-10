"""
Работа с сессиями
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

def make_engine_and_sessionmaker(database_url: str):
    """
    Получение асинхронного движка SQLAlchemy и фабрики сессий.
    """
    engine = create_async_engine(database_url, future=True)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    return engine, session_maker
