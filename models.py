from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str
    age: int
    phone_number: str

@dataclass
class Product:
    id: int
    name: str
    price: float
