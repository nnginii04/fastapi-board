from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

PAYLOAD = {"title": "Hello", "content": "First post", "author": "kim"}


def create_post() -> dict:
    response = client.post("/posts", json=PAYLOAD)
    assert response.status_code == 201
    return response.json()


def test_create_post():
    body = create_post()
    assert body["id"] > 0
    assert body["title"] == PAYLOAD["title"]
    assert body["content"] == PAYLOAD["content"]
    assert body["author"] == PAYLOAD["author"]


def test_read_post():
    created = create_post()
    response = client.get(f"/posts/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created


def test_replace_post():
    created = create_post()
    new = {"title": "Replaced", "content": "New body", "author": "lee"}
    response = client.put(f"/posts/{created['id']}", json=new)
    assert response.status_code == 200
    assert response.json() == {"id": created["id"], **new}
    assert client.get(f"/posts/{created['id']}").json() == {"id": created["id"], **new}


def test_replace_post_requires_all_fields():
    created = create_post()
    response = client.put(f"/posts/{created['id']}", json={"title": "Only title"})
    assert response.status_code == 422


def test_patch_post_partial():
    created = create_post()
    response = client.patch(f"/posts/{created['id']}", json={"title": "Patched"})
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Patched"
    assert body["content"] == PAYLOAD["content"]
    assert body["author"] == PAYLOAD["author"]


def test_patch_post_rejects_null_field():
    created = create_post()
    response = client.patch(f"/posts/{created['id']}", json={"title": None})
    assert response.status_code == 422


def test_delete_post():
    created = create_post()
    response = client.delete(f"/posts/{created['id']}")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/posts/{created['id']}").status_code == 404


def test_missing_post_returns_404():
    created = create_post()
    client.delete(f"/posts/{created['id']}")
    missing = f"/posts/{created['id']}"
    assert client.get(missing).status_code == 404
    assert client.put(missing, json=PAYLOAD).status_code == 404
    assert client.patch(missing, json={"title": "x"}).status_code == 404
    assert client.delete(missing).status_code == 404
