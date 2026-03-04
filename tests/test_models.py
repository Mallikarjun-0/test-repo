from dataclasses import asdict

import pytest

from models import Product, User


def test_user_creation_populates_all_fields() -> None:
    user = User(id=1, name="Alice Smith", email="alice@example.com", age=30)

    assert user.id == 1
    assert user.name == "Alice Smith"
    assert user.email == "alice@example.com"
    assert asdict(user) == {
        "id": 1,
        "name": "Alice Smith",
        "email": "alice@example.com",
        "age": 30,
    }


def test_user_equality_compares_every_field() -> None:
    baseline = User(id=1, name="Alice Smith", email="alice@example.com", age=30)

    assert baseline == User(id=1, name="Alice Smith", email="alice@example.com", age=30)
    assert baseline != User(id=2, name="Alice Smith", email="alice@example.com", age=30)
    assert baseline != User(id=1, name="Alice", email="alice@example.com", age=30)
    assert baseline != User(id=1, name="Alice Smith", email="alice@other.com", age=30)
    assert baseline != User(id=1, name="Alice Smith", email="alice@example.com", age=31)


def test_product_creation_populates_all_fields() -> None:
    product = Product(id=101, name="Laptop", price=999.99)

    assert product.id == 101
    assert product.name == "Laptop"
    assert product.price == pytest.approx(999.99)
    assert asdict(product) == {
        "id": 101,
        "name": "Laptop",
        "price": 999.99,
    }


def test_product_equality_compares_every_field() -> None:
    baseline = Product(id=101, name="Laptop", price=999.99)

    assert baseline == Product(id=101, name="Laptop", price=999.99)
    assert baseline != Product(id=102, name="Laptop", price=999.99)
    assert baseline != Product(id=101, name="Tablet", price=999.99)
    assert baseline != Product(id=101, name="Laptop", price=799.99)
