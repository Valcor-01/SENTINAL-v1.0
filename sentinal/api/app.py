"""Flask application factory and request-level wiring."""

import re
from uuid import uuid4

from flask import Flask, g, request

from sentinal.api.errors import register_error_handlers
from sentinal.api.routes.health import health_blueprint
from sentinal.config.settings import Settings
from sentinal.core.lifecycle import Lifecycle
from sentinal.core.logging import configure_logging, set_request_id
from sentinal.data.database import Database

_REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9._-]{1,128}$")


def create_app(
    settings: Settings | None = None,
    *,
    dotenv_path: str | None = None,
) -> Flask:
    """Create a configured, initialized application without starting a server."""
    active_settings = settings or Settings.from_env(dotenv_path=dotenv_path)
    logger = configure_logging(active_settings.log_level)

    app = Flask("sentinal")
    app.config.update(
        ENVIRONMENT=active_settings.environment,
        HOST=active_settings.host,
        PORT=active_settings.port,
        DEBUG=active_settings.debug,
        DATABASE_PATH=str(active_settings.database_path),
        LOG_LEVEL=active_settings.log_level,
        TESTING=active_settings.environment == "testing",
    )
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)
    app.logger.propagate = False

    database = Database(active_settings.database_path)
    database.initialize()
    lifecycle = Lifecycle(on_shutdown=database.close)
    lifecycle.startup()
    app.extensions["sentinal_database"] = database
    app.extensions["sentinal_lifecycle"] = lifecycle

    @app.before_request
    def bind_request_id() -> None:
        incoming = request.headers.get("X-Request-ID", "")
        request_id = incoming if _REQUEST_ID_PATTERN.fullmatch(incoming) else uuid4().hex
        g.request_id = request_id
        set_request_id(request_id)

    @app.after_request
    def add_request_id(response):
        response.headers["X-Request-ID"] = g.get("request_id", "-")
        return response

    register_error_handlers(app)
    app.register_blueprint(health_blueprint)
    return app
