from services import UserService, CatalogService
from database import db
from router import RouteNotFoundError, Router


def main():
    print("Starting application...")
    
    # Initialize services
    user_service = UserService()
    catalog_service = CatalogService()
    router = Router()

    @router.route("POST", "/users/{user_id}")
    def register_user_route(user_id: int, name: str, email: str, age: int):
        return user_service.register(user_id, name, email, age)

    @router.route("POST", "/products/{product_id}")
    def add_product_route(product_id: int, name: str, price: float):
        return catalog_service.add_product(product_id, name, price)

    # Use the services via router dispatch
    try:
        user = router.dispatch("POST", "/users/1", name="Alice Smith", email="alice@example.com", age=30)
        product = router.dispatch("POST", "/products/101", name="Laptop", price=999.99)
    except RouteNotFoundError as error:
        print(error)
        return
    
    print(f"Registered user: {user.name}")
    print(f"Added product: {product.name}")
    
    # Direct database access just to show another dependency edge
    all_users = len(db.users)
    print(f"Total users in DB: {all_users}")

if __name__ == "__main__":
    main()
