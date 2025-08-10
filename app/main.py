"""
Точка входа
"""

from fastapi import FastAPI
from app.core.config import Settings
from app.repository.sessions import make_engine_and_sessionmaker
from app.router import auth as auth_router_module


def create_app(settings: Settings | None = None) -> FastAPI:
    """
    Создать приложение
    """
    if settings is None:
        settings = Settings()

    app = FastAPI(title="Сервис Авторизации")

    engine, async_sessionmaker = make_engine_and_sessionmaker(settings.DATABASE_URL)
    app.state.engine = engine
    app.state.async_sessionmaker = async_sessionmaker
    app.state.settings = settings

    app.include_router(auth_router_module.router)

    @app.get("/")
    async def root():
        return {"message": "Запущен сервис авторизации"}

    return app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:create_app", factory=True, host="127.0.0.1", port=8000, reload=True)
