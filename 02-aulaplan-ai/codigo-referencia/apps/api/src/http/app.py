from flask import Flask

from src.auth.security import authenticate_request
from src.http.responses import register_error_handlers
from src.http.routes_ai import ai_bp
from src.http.routes_auth import users_bp
from src.http.routes_catalogs import catalogs_bp
from src.http.routes_health import health_bp
from src.http.routes_schedules import schedules_bp


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)
    app.config["TESTING"] = testing

    register_error_handlers(app)

    if not testing:
        app.before_request(authenticate_request)

    app.register_blueprint(health_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(catalogs_bp)
    app.register_blueprint(schedules_bp)
    app.register_blueprint(ai_bp)

    return app
