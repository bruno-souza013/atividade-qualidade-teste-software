users = []
current_id = 1


def get_all_users():
    return users


def get_user_by_id(user_id):
    return next((u for u in users if u["id"] == user_id), None)


def create_user(data):
    global current_id
    user = {"id": current_id, "name": data["name"]}
    users.append(user)
    current_id += 1
    return user


def update_user(user_id, data):
    user = get_user_by_id(user_id)
    if not user:
        return None

    user["name"] = data["name"]
    return user


def delete_user(user_id):
    global users
    users = [u for u in users if u["id"] != user_id]
