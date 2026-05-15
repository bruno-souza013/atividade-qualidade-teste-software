import pytest
from app import create_app
from app.services import user_services


@pytest.fixture
def client():
    app = create_app()
    user_services.users.clear()
    user_services.current_id = 1

    return app.test_client()


def test_user_flow(client):

    response = client.post("/users", json={"name": "Bruno Lopes"})
    assert response.status_code == 201

    user = response.get_json()
    user_id = user["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200

    response = client.put(f"/users/{user_id}", json={"name": "Souza"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "Souza"

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404


def test_list_users(client):
    client.post("/users", json={"name": "User1"})
    client.post("/users", json={"name": "User2"})

    response = client.get("/users")

    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2


def test_list_three_users(client):
    client.post("/users", json={"name": "User1"})
    client.post("/users", json={"name": "User2"})
    client.post("/users", json={"name": "User3"})

    response = client.get("/users")

    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 3
