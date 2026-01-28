from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)


def test_create_user():
    email = f"user_{uuid.uuid4()}@gmail.com"

    response = client.post(
        "/user",
        json={
            "username": "Test User",
            "email": email,
            "password": "testpassword"
        }
    )

    assert response.status_code in (200, 201)
    assert response.json()["email"] == email


def test_get_user_by_id():
    email = f"user_{uuid.uuid4()}@gmail.com"

    create_response = client.post(
        "/user",
        json={
            "username": "Fetch User",
            "email": email,
            "password": "fetchpassword"
        }
    )

    assert create_response.status_code in (200, 201)

    user_id = create_response.json()["id"]

    response = client.get(f"/user/{user_id}")

    assert response.status_code == 200
    assert response.json()["email"] == email

def test_create_user_duplicate_email():
    import uuid
    email = f"dup_{uuid.uuid4()}@gmail.com"

    # First creation → should succeed
    response1 = client.post(
        "/user",
        json={
            "username": "User One",
            "email": email,
            "password": "password123"
        }
    )

    assert response1.status_code in (200, 201)

    # Second creation with SAME email → should fail
    response2 = client.post(
        "/user",
        json={
            "username": "User Two",
            "email": email,
            "password": "password456"
        }
    )

    assert response2.status_code == 409


def test_get_user_not_found():
    response = client.get("/user/999999")
    assert response.status_code == 404

