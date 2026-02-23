from typing import List, Optional

from models import User, Product


class Database:
    def __init__(self):
        self.users: List[User] = []
        self.products: List[Product] = []

    def save_user(self, user: User) -> None:
        self.users.append(user)

    def get_user(self, user_id: int) -> Optional[User]:
        return next((u for u in self.users if u.id == user_id), None)

    def save_product(self, product: Product) -> None:
        self.products.append(product)

    def get_product(self, product_id: int) -> Optional[Product]:
        return next((p for p in self.products if p.id == product_id), None)

db = Database()
