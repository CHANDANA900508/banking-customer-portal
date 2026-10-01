import sys
import os
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
from app.app import app
def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Banking Customer Portal is running" in response.data
def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "UP"
def test_register_customer():
    client = app.test_client()
    response = client.post(
        "/customers",
        json={
            "name": "Chandana",
            "email": "chandana@example.com"
        }
    )
    assert response.status_code == 201
    assert response.json["name"] == "Chandana"