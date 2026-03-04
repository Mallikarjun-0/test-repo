from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, Pattern, Tuple


Handler = Callable[..., Any]
_PATH_PARAMETER = re.compile(r"\{(?P<name>[a-zA-Z_]\w*)\}")


class RouteNotFoundError(Exception):
    """Raised when dispatch cannot find a matching handler for a request."""


class DuplicateRouteError(Exception):
    """Raised when attempting to register a route that already exists."""


@dataclass(frozen=True)
class RouteInfo:
    method: str
    template: str
    parameter_names: Tuple[str, ...]


@dataclass(frozen=True)
class _Route:
    method: str
    template: str
    handler: Handler
    pattern: Pattern[str]

    @property
    def parameter_names(self) -> Tuple[str, ...]:
        return tuple(self.pattern.groupindex.keys())


class Router:
    """HTTP-style router that supports path parameters."""

    def __init__(self) -> None:
        self._routes: Dict[str, Dict[str, _Route]] = {}

    def register(self, method: str, path: str, handler: Handler) -> Handler:
        method_key = method.upper()
        template = self._normalize_path(path)
        method_registry = self._routes.setdefault(method_key, {})
        if template in method_registry:
            raise DuplicateRouteError(f"Route already registered for {method_key} {template}")
        method_registry[template] = _Route(
            method=method_key,
            template=template,
            handler=handler,
            pattern=self._compile_pattern(template),
        )
        return handler

    def route(self, method: str, path: str) -> Callable[[Handler], Handler]:
        def decorator(handler: Handler) -> Handler:
            self.register(method, path, handler)
            return handler

        return decorator

    def dispatch(self, method: str, path: str, **kwargs: Any) -> Any:
        method_key = method.upper()
        normalized_path = self._normalize_path(path)
        for route in self._routes.get(method_key, {}).values():
            match = route.pattern.match(normalized_path)
            if match:
                params = {**match.groupdict(), **kwargs}
                return route.handler(**params)
        raise RouteNotFoundError(f"No route for {method_key} {normalized_path}")

    def list_routes(self) -> Tuple[RouteInfo, ...]:
        return tuple(
            RouteInfo(method=route.method, template=route.template, parameter_names=route.parameter_names)
            for routes_by_template in self._routes.values()
            for route in routes_by_template.values()
        )

    def register_many(self, routes: Iterable[Tuple[str, str, Handler]]) -> None:
        for method, path, handler in routes:
            self.register(method, path, handler)

    def __len__(self) -> int:
        return sum(len(routes) for routes in self._routes.values())

    @staticmethod
    def _normalize_path(path: str) -> str:
        normalized = path.strip()
        if not normalized.startswith("/"):
            normalized = f"/{normalized}"
        if len(normalized) > 1 and normalized.endswith("/"):
            normalized = normalized[:-1]
        return normalized

    @staticmethod
    def _compile_pattern(template: str) -> Pattern[str]:
        regex = _PATH_PARAMETER.sub(lambda match: f"(?P<{match.group('name')}>[^/]+)", template)
        return re.compile(f"^{regex}$")