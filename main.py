from test_python_deps.services import UserService, CatalogService
from test_python_deps.database import db


def main():
    print("Starting application...")
    
    # Initialize services
    user_service = UserService()
    catalog_service = CatalogService()
    
    # Use the services
    user = user_service.register(1, "Alice Smith", "alice@example.com")
    product = catalog_service.add_product(101, "Laptop", 999.99)
    
    print(f"Registered user: {user.name}")
    print(f"Added product: {product.name}")
    
    # Direct database access just to show another dependency edge
    all_users = len(db.users)
    print(f"Total users in DB: {all_users}")

if __name__ == "__main__":
    main()
