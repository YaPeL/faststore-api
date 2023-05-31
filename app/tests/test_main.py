from app.main import app
from app.database import get_db
from fastapi.testclient import TestClient


class FakeDB:
    def __init__(self):
        self.data = []

    def add(self, item):
        item.id = 1

    def commit(self):
        pass

    def refresh(self, item):
        pass


app.dependency_overrides[get_db] = lambda: FakeDB()

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


jason = {"title": "string", "sku": "string", "images": "string", "category": "string", "tags": "string"}


def test_fake_db():
    response = client.post("/api/v1/products", json=jason)
    assert response.status_code == 200
    jason["id"] = 1
    jason["inventory_quantity"] = 0
    assert response.json() == jason
