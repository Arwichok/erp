from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from litestar import Litestar



def create_app() -> Litestar:
    from litestar import Litestar
    from .config import plugins, on_startup, stores, dependencies, on_app_init
    from .controllers import route_handlers

    return Litestar(
        route_handlers,
        plugins=plugins,
        on_startup=on_startup,
        stores=stores,
        dependencies=dependencies,
        on_app_init=on_app_init,
    )
