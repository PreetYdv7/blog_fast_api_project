from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_login():
    response = client.post("/login",
    json = {
        "username": "preetyadav0099@gmail.com",
        "password": "Preet@2003"
    })
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password():
    response = client.post(
        "/login",
        json={
            "username": "admin",
            "password": "wrong password"
        }
    )

    assert response.status_code == 404

def test_login_missing_password():
    response = client.post(
        "/login",
        json={
            "username": "admin"
        }
    )

    assert response.status_code == 422





