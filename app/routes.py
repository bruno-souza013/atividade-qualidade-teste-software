from flask import Blueprint, jsonify

main = Blueprint("main", __name__)


@main.route("/status", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})


@main.route("/hello", methods=["GET"])
def say_hello():
    return jsonify({"message": "Hello World"})
