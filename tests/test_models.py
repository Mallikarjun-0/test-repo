import dataclasses

from models import Product, User


def test_user_creation_sets_all_fields():
    user = User(id=1, name="Alice", email="alice@example.com")

    assert user.id == 1
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert dataclasses.asdict(user) == {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
    }


def test_user_equality_depends_on_all_fields():
    reference = User(id=2, name="Bob", email="bob@example.com")
    same_values = User(id=2, name="Bob", email="bob@example.com")
    different_email = User(id=2, name="Bob", email="other@example.com")

    assert reference == same_values
    assert reference != different_email


def test_product_creation_sets_all_fields():
    product = Product(id=101, name="Laptop", price=999.99)

    assert product.id == 101
    assert product.name == "Laptop"
    assert product.price == 999.99
    assert isinstance(product.price, float)


def test_product_equality_depends_on_all_fields():
    reference = Product(id=5, name="Keyboard", price=49.99)
    same_values = Product(id=5, name="Keyboard", price=49.99)
    different_price = Product(id=5, name="Keyboard", price=59.99)

    assert reference == same_values
    assert reference != different_price
