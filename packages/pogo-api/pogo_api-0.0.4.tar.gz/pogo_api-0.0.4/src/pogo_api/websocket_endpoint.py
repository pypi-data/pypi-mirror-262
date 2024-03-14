from typing import Callable, Coroutine

from pogo_api.pascal_converter import pascal_to_kebab
from pogo_api.pascal_converter import pascal_to_name
from pogo_api.websocket_route import WebSocket


class WebSocketEndpoint:
    endpoint: Callable[..., Coroutine]

    @property
    def path(self) -> str:
        kebab_case = pascal_to_kebab(pascal=self.__class__.__name__)
        return f"/{kebab_case}"

    @property
    def name(self) -> str:
        return pascal_to_name(self.__class__.__name__)

    @property
    def route(self) -> WebSocket:
        return WebSocket(
            path=self.path,
            endpoint=self.endpoint,
            name=self.name,
        )
