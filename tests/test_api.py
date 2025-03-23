import asyncio
import pathlib
import sys
from collections.abc import AsyncIterator
from os import getenv
import time

from faker import Faker
import httpx
import httpx_sse
import pytest
from litestar import Litestar
from litestar.testing import AsyncTestClient, subprocess_async_client

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


from app import create_app


faker = Faker()

TEST_USER = {
    "email": "V2k0p@example.com",
    "password": "password",
    "name": "John Doe",
}


@pytest.fixture(scope="function")
async def client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    app = create_app()
    app.debug = True
    async with AsyncTestClient(app=app, base_url="http://host.local:8000/api") as client:
        yield client


async def test_users(client: AsyncTestClient[Litestar]) -> None:
    response = await client.get("/users")
    assert response.status_code == 200


async def test_signup(
        client: AsyncTestClient[Litestar],
        user: dict[str, str] = TEST_USER
) -> None:
    response = await client.post("/signup", json=user)
    assert response.status_code == 201


async def test_login(client: AsyncTestClient[Litestar],
                     user: dict[str, str] = TEST_USER
) -> None:
    response = await client.post("/login", json=dict(
        email=user["email"],
        password=user["password"],
    ))
    assert response.status_code == 201

    response = await client.get("/user")
    assert response.status_code == 200
    user = response.json()
    assert user.get("email") == user["email"]
    assert user.get("name") == user["name"]

