from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, Tuple


Handler = Callable[..., Any]


class RouteNotFoundError(Exception):
    """Raised when dispatch finds no registered handler for a route."""


class DuplicateRouteError(Exception):
    """Raised when trying to register a route that already exists."""


@dataclass(frozen=True)
class RouteKey:
    method: str
    path: str

    def __post_init__(self) -> None:
        normalized_method = self.method.upper()
        normalized_path = self.path if self.path.startswith("/") else f"/{self.path}"
        object.__setattr__(self, "method", normalized_method)
        object.__setattr__(self, "path", normalized_path)


class Router:
    """Simple HTTP-style router that dispatches handlers by method and path."""

    def __init__(self) -> None:
        self._routes: Dict[RouteKey, Handler] = {}

    def register(self, method: str, path: str, handler: Handler) -> Handler:
        """Register a handler for the supplied HTTP-style method/path."""

        key = RouteKey(method, path)
        if key in self._routes:
            raise DuplicateRouteError(f"Route already registered: {key}")
        self._routes[key] = handler
        return handler

    def route(self, method: str, path: str) -> Callable[[Handler], Handler]:
        """Decorator-style helper that registers a handler for a route."""

        def decorator(handler: Handler) -> Handler:
            self.register(method, path, handler)
            return handler

        return decorator

    def dispatch(self, method: str, path: str, **kwargs: Any) -> Any:
        """Call the handler registered for the method/path."""

        key = RouteKey(method, path)
        handler = self._routes.get(key)
        if handler is None:
            raise RouteNotFoundError(f"No handler registered for {key}")
        return handler(**kwargs)

    def list_routes(self) -> Tuple[RouteKey, ...]:
        """Return all registered routes."""

        return tuple(self._routes.keys())

    def register_many(self, routes: Iterable[Tuple[str, str, Handler]]) -> None:
        """Bulk register handlers from an iterable of (method, path, handler)."""

        for method, path, handler in routes:
            self.register(method, path, handler)

    def __len__(self) -> int:
        return len(self._routes)