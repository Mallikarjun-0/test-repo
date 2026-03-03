from __future__ import annotations

from typing import Any, Callable, Dict, Tuple


Handler = Callable[..., Any]


class RouteNotFoundError(Exception):
    pass


class DuplicateRouteError(Exception):
    pass


class Router:
    def __init__(self) -> None:
        self._routes: Dict[Tuple[str, str], Handler] = {}

    def register(self, method: str, path: str, handler: Handler) -> None:
        normalized = (method.upper(), self._normalize_path(path))
        if normalized in self._routes:
            raise DuplicateRouteError(f"Route already registered for {normalized}")
        self._routes[normalized] = handler

    def route(self, method: str, path: str) -> Callable[[Handler], Handler]:
        def decorator(handler: Handler) -> Handler:
            self.register(method, path, handler)
            return handler

        return decorator

    def dispatch(self, method: str, path: str, **kwargs: Any) -> Any:
        key = (method.upper(), self._normalize_path(path))
        handler = self._routes.get(key)
        if handler is None:
            raise RouteNotFoundError(f"No handler for {key}")
        return handler(**kwargs)

    def list_routes(self) -> Tuple[Tuple[str, str], ...]:
        return tuple(self._routes.keys())

    @staticmethod
    def _normalize_path(path: str) -> str:
        return path if path.startswith("/") else f"/{path}"