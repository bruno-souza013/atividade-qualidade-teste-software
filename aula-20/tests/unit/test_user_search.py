from app.services import user_services


def setup_function():
    user_services.users.clear()
    user_services.current_id = 1


def test_search_exact_name():
    user_services.create_user({"name": "Ana"})
    user_services.create_user({"name": "Rafael"})

    results = user_services.search_users("Ana")
    assert len(results) == 1
    assert results[0]["name"] == "Ana"


def test_search_case_insensitive():
    user_services.create_user({"name": "Carla"})
    results = user_services.search_users("carla")
    assert len(results) == 1


def test_search_substring():
    user_services.create_user({"name": "Daniela"})
    results = user_services.search_users("ani")
    assert len(results) == 1


def test_search_no_results():
    user_services.create_user({"name": "Sofia"})
    results = user_services.search_users("zzzz")
    assert results == []


def test_search_empty_returns_all():
    user_services.create_user({"name": "João"})
    user_services.create_user({"name": "Silva"})
    results = user_services.search_users("")
    assert len(results) == 2


def test_search_multiple_matches():
    user_services.create_user({"name": "Ana"})
    user_services.create_user({"name": "Analu"})
    user_services.create_user({"name": "An"})

    results = user_services.search_users("an")
    assert len(results) == 3


def test_search_after_delete():
    u = user_services.create_user({"name": "Lucas"})
    user_services.create_user({"name": "Felipe"})

    user_services.delete_user(u["id"])
    results = user_services.search_users("Lucas")
    assert results == []


def test_search_strip_whitespace():
    user_services.create_user({"name": "Mariana"})
    results = user_services.search_users("  Mariana  ")
    assert len(results) == 1


def test_search_special_characters():
    user_services.create_user({"name": "Souza ++"})
    results = user_services.search_users("Souza ++")
    assert len(results) == 1
