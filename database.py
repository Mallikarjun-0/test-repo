from __future__ import annotations

from typing import Dict, Generic, Optional, Protocol, Tuple, TypeVar

from models import Product, User


class HasId(Protocol):
    id: int


T = TypeVar("T", bound=HasId)


class InMemoryRepository(Generic[T]):
    def __init__(self) -> None:
        self._items: Dict[int, T] = {}

    def save(self, item: T) -> None:
        self._items[item.id] = item

    def get(self, item_id: int) -> Optional[T]:
        return self._items.get(item_id)

    def list_all(self) -> Tuple[T, ...]:
        return tuple(self._items.values())

    def __len__(self) -> int:
        return len(self._items)


class Database:
    def __init__(self) -> None:
        self._users: InMemoryRepository[User] = InMemoryRepository()
        self._products: InMemoryRepository[Product] = InMemoryRepository()

    def save_user(self, user: User) -> None:
        self._users.save(user)

    def get_user(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    def save_product(self, product: Product) -> None:
        self._products.save(product)

    def get_product(self, product_id: int) -> Optional[Product]:
        return self._products.get(product_id)

    @property
    def users(self) -> Tuple[User, ...]:
        return self._users.list_all()

    @property
    def products(self) -> Tuple[Product, ...]:
        return self._products.list_all()


db = Database()