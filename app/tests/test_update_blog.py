
from app.tests.utils import get_token, client




def test_update_blog():
    token = get_token()

    # create blog (Blog schema → needs user_id)
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

    # update blog (BlogBase schema → NO user_id)
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
