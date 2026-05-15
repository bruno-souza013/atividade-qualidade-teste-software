def test_should_not_allow_duplicate_users():
    from app.services import user_services
    
    user_services.users.clear()
    user_services.current_id = 1
    
    user_services.create_user({"name": "Bruno"})
    
    user = user_services.create_user({"name" : "Bruno"})
    
    assert user is None
    