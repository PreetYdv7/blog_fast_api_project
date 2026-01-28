from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def get_token():
    response = client.post(
        "/login",
        json={
            "username": "preetyadav0099@gmail.com",
            "password": "Preet@2003"
        }
    )
    return response.json()["access_token"]