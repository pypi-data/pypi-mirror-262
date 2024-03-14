from dataclasses import dataclass
from typing import Callable

from fastapi import APIRouter
from fastapi import FastAPI


@dataclass
class WebSocket:
    path: str
    endpoint: Callable
    name: str

    def add_to_router(self, router: APIRouter | FastAPI) -> None:
        router.add_api_websocket_route(
            path=self.path,
            endpoint=self.endpoint,
            name=self.name,
        )
