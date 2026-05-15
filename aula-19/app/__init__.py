from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    from app.routes.user_routes import user_bp

    app.register_blueprint(user_bp)

    @app.route("/")
    def index():
        return render_template("users.html")

    return app
