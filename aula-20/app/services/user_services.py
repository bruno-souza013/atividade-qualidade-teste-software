users = []
current_id = 1


def get_all_users():
    return users


def get_user_by_id(user_id):
    return next((u for u in users if u["id"] == user_id), None)


def update_user(user_id, data):
    user = get_user_by_id(user_id)
    if not user:
        return None

    user["name"] = data["name"]
    return user


def delete_user(user_id):
    global users
    users = [u for u in users if u["id"] != user_id]


def search_users(name: str):
    if name is None:
        return users

    q = name.strip().lower()
    if q == "":
        return users

    return [u for u in users if q in u["name"].lower()]


def create_user(data):
    """Create a new user unless a user with the same name exists.

    Returns the new user dict on success, or None if duplicate.
    """
    global current_id

    existing_user = next((u for u in users if u["name"] == data["name"]), None)
    if existing_user:
        return None

    user = {"id": current_id, "name": data["name"]}
    users.append(user)
    current_id += 1
    return user
