from app import create_app
from app.services import user_services


def setup_function():
    user_services.users.clear()
    user_services.current_id = 1


def test_search_route_filters_by_name():
    app = create_app()
    client = app.test_client()

    client.post("/users", json={"name": "Joao"})
    client.post("/users", json={"name": "Lucas"})
    client.post("/users", json={"name": "Gabriel"})

    resp = client.get("/users?name=ann")
    assert resp.status_code == 200
    data = resp.get_json()
    names = [u["name"] for u in data]
    assert "Joao" in names and "Lucas" in names
    assert "Gabriel" not in names

def setup_function():
    user_services.users.clear()
    user_services.current_id = 1


def test_get_users_returns_all():
    app = create_app()
    client = app.test_client()

    client.post("/users", json={"name": "João"})
    client.post("/users", json={"name": "Miguel"})

    resp = client.get("/users")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 2


def test_post_duplicate_returns_400():
    app = create_app()
    client = app.test_client()

    client.post("/users", json={"name": "Lucas"})
    resp = client.post("/users", json={"name": "Lucas"})
    assert resp.status_code == 400


def test_put_update_user():
    app = create_app()
    client = app.test_client()

    resp = client.post("/users", json={"name": "Pedro"})
    assert resp.status_code == 201
    user = resp.get_json()
    uid = user["id"]

    resp2 = client.put(f"/users/{uid}", json={"name": "Pedro Silva"})
    assert resp2.status_code == 200
    assert resp2.get_json()["name"] == "Pedro Silva"


def test_delete_nonexistent_returns_404():
    app = create_app()
    client = app.test_client()

    resp = client.delete("/users/9999")
    assert resp.status_code == 404
