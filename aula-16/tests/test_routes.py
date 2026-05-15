import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    return app.test_client()


def test_create_user_success(client):
    response = client.post("/users", json={"name": "Bruno Lopes"})

    assert response.status_code == 201
    assert response.get_json()["name"] == "Bruno Lopes"


def test_create_user_without_name(client):
    response = client.post("/users", json={})

    assert response.status_code == 400
    assert "name is required" in str(response.data)


def test_get_user(client):
    client.post("/user", json={"name": "Teste"})

    response = client.get("/users/1")

    assert response.status_code == 200


def test_get_user_not_found(client):
    response = client.get("/users/999")

    assert response.status_code == 404
    assert "User not found" in str(response.data)


def test_delete_user(client):
    client.post("/user", json={"name": "Delete"})

    response = client.delete("/users/1")

    assert response.status_code == 204


def test_update_user_success(client):

    response = client.post("/users", json={"name": "Bruno Lopes"})
    assert response.status_code == 201

    user_id = response.get_json()["id"]

    response = client.put(f"/users/{user_id}", json={"name": "Souza"})

    assert response.status_code == 200
    assert response.get_json()["name"] == "Souza"
