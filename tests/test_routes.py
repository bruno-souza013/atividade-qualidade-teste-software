from app import create_app


def test_health_check():
    app = create_app()
    client = app.test_client()

    response = client.get("/status")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_say_hello():
    app = create_app()
    client = app.test_client()

    response = client.get("/hello")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello World"}
