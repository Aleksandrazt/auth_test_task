"""
Тестир
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import create_app
from app.core.config import Settings
from app.models.base import Base


DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="session")
async def prepare_database():
    engine = create_async_engine(DATABASE_URL, echo=False, future=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine, async_session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def client(prepare_database):
    engine, async_session = prepare_database

    test_settings = Settings(DATABASE_URL=DATABASE_URL)
    app = create_app(test_settings)
    app.state.engine = engine
    app.state.async_sessionmaker = async_session

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Запущен сервис авторизации"}


@pytest.mark.asyncio
async def test_signup_and_login(client):
    signup_data = {"email": "test@example.com", "password": "secret"}
    response = await client.post("/auth/signup", json=signup_data)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

    login_data = {"username": "test@example.com", "password": "secret"}
    response = await client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
