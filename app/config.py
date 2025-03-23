from __future__ import annotations

from pathlib import Path
from pprint import pprint
from typing import TYPE_CHECKING, Any

from environs import Env
from litestar import Request
from litestar.connection import ASGIConnection
from litestar.di import Provide
from litestar.middleware.session.server_side import (
    ServerSideSessionBackend,
    ServerSideSessionConfig,
)
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar_browser_reload import BrowserReloadPlugin
from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin
from litestar.security.session_auth.auth import SessionAuth
from litestar.stores.memory import MemoryStore
from litestar.stores.file import FileStore
from litestar.stores.registry import StoreRegistry
from sqlalchemy.ext.asyncio import AsyncSession
from watchfiles import DefaultFilter

from .models import User, metadata
from .repos import UserRepository


if TYPE_CHECKING:
    from litestar import Litestar

env = Env()
DB_URL = env.str("DB_URL", "sqlite+aiosqlite:///db.sqlite3")
APP_PATH = Path(__file__).parent
ROOT_PATH = APP_PATH.parent
TEMPLATES_PATH = APP_PATH / "controllers" / "templates"


async def sqlalchemy_init(app: Litestar) -> None:
    async with sqlalchemy_config.get_engine().begin() as conn:
        await conn.run_sync(metadata.create_all)


async def retrieve_user_handler(
    session: dict[str, Any], connection: "ASGIConnection[Any, Any, Any, Any]"
) -> User | None:
    if user_id := session.get("user_id"):
        async with sqlalchemy_config.get_session() as db_session:
            return await db_session.get(User, user_id)


sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=DB_URL,
    create_all=True,
    metadata=metadata,
)
sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)

template_config=TemplateConfig(
    directory=TEMPLATES_PATH,
    engine=JinjaTemplateEngine
)
browser_reload_plugin = BrowserReloadPlugin(
    watch_paths=(TEMPLATES_PATH,),
    watch_filter=DefaultFilter(ignore_dirs=(".git", ".hg", ".svn", ".tox")),
)
session_auth = SessionAuth[User, ServerSideSessionBackend](
    retrieve_user_handler=retrieve_user_handler,
    session_backend_config=ServerSideSessionConfig(),
    exclude=["/login", "/signup", "/"],
)

memory_store = MemoryStore()

def default_store(name: str):
    return memory_store

stores = StoreRegistry(
    stores={
        "memory": memory_store,
        "session": memory_store,
    },
    default_factory=default_store
)
plugins = [sqlalchemy_plugin, browser_reload_plugin]
on_startup = [sqlalchemy_init]
on_app_init = [session_auth.on_app_init]
dependencies = {}
