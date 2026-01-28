
from app.tests.utils import get_token, client


def test_delete_blog_owner():
    token = get_token()

    # create blog first
    create_response = client.post(
        "/blog",
        json={
            "title": "Delete Me",
            "body": "To be deleted",
            "user_id": 1
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert create_response.status_code in (200, 201)

    blog_id = create_response.json()["id"]

    # delete blog
    response = client.delete(
        f"/blog/{blog_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code in (200, 202, 204)

def test_delete_blog_without_token():
    response = client.delete("/blog/1")
    assert response.status_code == 401


def test_delete_blog_twice():
    token = get_token()

    create_response = client.post(
        "/blog",
        json={
            "title": "Delete Twice",
            "body": "Test",
            "user_id": 1
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    blog_id = create_response.json()["id"]

    # first delete
    response1 = client.delete(
        f"/blog/{blog_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response1.status_code in (200, 202, 204)

    # second delete
    response2 = client.delete(
        f"/blog/{blog_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response2.status_code == 404

