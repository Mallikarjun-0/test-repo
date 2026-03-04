from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str
    age: int

@dataclass
class Product:
    id: int
    name: str
    price: float
