
from app.tests.utils import get_token, client




def test_create_blog():
    token = get_token()

    response = client.post(
        "/blog",
        json={
            'user_id' : 0,
            "title": "My First Blog",
            "body": "This is a test blog"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code in (200, 201)
    assert response.json()["title"] == "My First Blog"

def test_create_blog_without_token():
    response = client.post(
        "/blog",
        json={
            "title": "No Auth Blog",
            "body": "Should fail"
        }
    )

    assert response.status_code == 401


def test_get_all_blogs():
    token = get_token()

    response = client.get(
        "/blog/blogs",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_blog_by_id():
    token = get_token()

    create_response = client.post(
        "/blog",
        json={
            "title": "Fetch Blog",
            "body": "Fetch body",
            "user_id" : 0
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    blog_id = create_response.json()["id"]

    response = client.get(f"/blog/{blog_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Fetch Blog"

def test_update_blog():
    token = get_token()

    # create a blog first
    create_response = client.post(
        "/blog",
        json={
            "title": "Old Title",
            "body": "Old Body",
            "user_id": 1
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert create_response.status_code in (200, 201)

    blog_id = create_response.json()["id"]

    # update the blog
    response = client.put(
        f"/blog/{blog_id}",
        json={
            "title": "New Title",
            "body": "New Body"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code in (200, 202)
    assert response.json()["title"] == "New Title"

