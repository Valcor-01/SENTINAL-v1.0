"""Application readiness endpoint."""

from flask import Blueprint, current_app, jsonify

from sentinal import __version__
from sentinal.core.exceptions import ApplicationError
from sentinal.core.lifecycle import LifecycleState
from sentinal.core.models import HealthStatus

health_blueprint = Blueprint("health", __name__)


@health_blueprint.get("/api/health")
def health():
    lifecycle = current_app.extensions["sentinal_lifecycle"]
    database = current_app.extensions["sentinal_database"]
    if lifecycle.state is not LifecycleState.RUNNING or not database.health():
        raise ApplicationError("The application is not ready.")
    status = HealthStatus(status="healthy", version=__version__)
    return jsonify(
        data={"status": status.status, "version": status.version}, meta={"service": "sentinal"}
    )
