from math import isclose

from models import Product, User


def test_user_initialization_sets_all_fields():
    user = User(id=1, name="Alice", email="alice@example.com")

    assert user.id == 1
    assert user.name == "Alice"
    assert user.email == "alice@example.com"


def test_user_equality_is_based_on_field_values():
    left = User(id=1, name="Alice", email="alice@example.com")
    right = User(id=1, name="Alice", email="alice@example.com")
    different = User(id=2, name="Alice", email="alice@example.com")

    assert left == right
    assert left != different


def test_product_initialization_sets_all_fields():
    product = Product(id=10, name="Laptop", price=999.99)

    assert product.id == 10
    assert product.name == "Laptop"
    assert isclose(product.price, 999.99)


def test_product_equality_is_based_on_all_fields():
    reference = Product(id=10, name="Laptop", price=999.99)
    same = Product(id=10, name="Laptop", price=999.99)
    different_price = Product(id=10, name="Laptop", price=1099.99)
    different_name = Product(id=10, name="Desktop", price=999.99)
    different_id = Product(id=11, name="Laptop", price=999.99)

    assert reference == same
    assert reference != different_price
    assert reference != different_name
    assert reference != different_id
