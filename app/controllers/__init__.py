from .api import APIController
from .web import WebController

__all__ = ["route_handlers"]


route_handlers = [
    APIController,
    WebController
]

