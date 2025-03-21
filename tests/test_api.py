import asyncio
import pathlib
import sys
from collections.abc import AsyncIterator
from os import getenv

import httpx
import httpx_sse
import pytest
from litestar import Litestar
from litestar.testing import AsyncTestClient, subprocess_async_client

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


from app import create_app



@pytest.fixture(scope="function")
async def client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    app = create_app()
    app.debug = True
    async with AsyncTestClient(app=app) as client:
        yield client


async def test_users(client: AsyncTestClient[Litestar]) -> None:

    response = await client.get("/users")

    assert response.status_code == 200
