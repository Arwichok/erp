from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from litestar import Litestar


def create_app() -> Litestar:
    from litestar import Litestar
    from litestar.plugins.htmx import HTMXRequest

    from .config import (
        dependencies,
        on_app_init,
        on_startup,
        plugins,
        stores,
        template_config,
    )
    from .controllers import route_handlers

    return Litestar(
        route_handlers,
        plugins=plugins,
        on_startup=on_startup,
        stores=stores,
        dependencies=dependencies,
        on_app_init=on_app_init,
        request_class=HTMXRequest,
        template_config=template_config,
    )
