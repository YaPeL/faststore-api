import pytest
from sqlalchemy.orm import Session

from app.main import app, get_db


@pytest.fixture(scope="module")
def test_app():
    # Create a TestClient instance using the FastAPI app
    client = TestClient(app)
    # Provide the TestClient as a dependency for the test functions
    app.dependency_overrides[get_db] = override_dependency(client)
    yield client  # Yield the TestClient instance

@pytest.fixture(scope="module")
def db():
    # Create and set up a test database connection (e.g., using SQLite)
    # Initialize the database tables with test data
    # Return the database connection
    yield db  # Close the database connection after the tests

def test_create_product(test_app: TestClient, db: Session):
    # Define the test payload for creating a product
    product_data = {
        "title": "Test Product",
        "sku": "ABC123",
        "images": "image1.jpg,image2.jpg",
        "category": "Test Category",
        "tags": "tag1,tag2"
    }
    # Make a POST request to the create_product endpoint
    response = test_app.post("/products/", json=product_data)
    assert response.status_code == 200
    # Verify that the product is created and returned in the response
    product = response.json()
    assert product["title"] == product_data["title"]
    assert product["sku"] == product_data["sku"]

def test_get_product(test_app: TestClient, db: Session):
    # Make a GET request to the get_product endpoint with a known product_id
    product_id = 1
    response = test_app.get(f"/products/{product_id}")
    assert response.status_code == 200
    # Verify that the correct product is returned in the response
    product = response.json()
    assert product["id"] == product_id