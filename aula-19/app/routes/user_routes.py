from flask import Blueprint, request, jsonify
from app.services.user_services import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user,
)

user_bp = Blueprint("users", __name__, url_prefix="/users")


@user_bp.route("", methods=["GET"])
def list_users():
    return jsonify(get_all_users()), 200


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


@user_bp.route("", methods=["POST"])
def create():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400

    user = create_user(data)
    return jsonify(user), 201


@user_bp.route("/<int:user_id>", methods=["PUT"])
def update(user_id):
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400
    user = update_user(user_id, data)

    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete(user_id):
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404
    delete_user(user_id)
    return "", 204
