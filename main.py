from services import UserService, CatalogService
from database import db
from router import RouteNotFoundError, Router


def main():
    print("Starting application...")
    
    # Initialize services
    user_service = UserService()
    catalog_service = CatalogService()
    router = Router()

    def register_user_route(user_id: int, name: str, email: str):
        return user_service.register(user_id, name, email)

    def add_product_route(product_id: int, name: str, price: float):
        return catalog_service.add_product(product_id, name, price)

    router.register("POST", "/users", register_user_route)
    router.register("POST", "/products", add_product_route)
    
    # Use the services
    try:
        user = router.dispatch("POST", "/users", user_id=1, name="Alice Smith", email="alice@example.com")
        product = router.dispatch("POST", "/products", product_id=101, name="Laptop", price=999.99)
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
