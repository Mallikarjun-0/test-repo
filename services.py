from models import User, Product
from database import db


class UserService:
    def register(self, user_id: int, name: str, email: str, age: int, phone_number: str) -> User:
        user = User(id=user_id, name=name, email=email, age=age, phone_number=phone_number)
        db.save_user(user)
        return user

class CatalogService:
    def add_product(self, product_id: int, name: str, price: float) -> Product:
        product = Product(id=product_id, name=name, price=price)
        db.save_product(product)
        return product
