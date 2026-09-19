"""Safe, consistent Flask error responses."""

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from sentinal.core.exceptions import ApplicationError, DatabaseError
from sentinal.core.logging import get_request_id


def error_response(code: str, message: str, status_code: int):
    return (
        jsonify(
            error={"code": code, "message": message, "request_id": get_request_id()},
            meta={"service": "sentinal"},
        ),
        status_code,
    )


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(_: HTTPException):
        return error_response("not_found", "The requested resource was not found.", 404)

    @app.errorhandler(405)
    def method_not_allowed(_: HTTPException):
        return error_response("method_not_allowed", "The request method is not allowed.", 405)

    @app.errorhandler(ApplicationError)
    def application_error(error: ApplicationError):
        return error_response(error.code, str(error), error.status_code)

    @app.errorhandler(DatabaseError)
    def database_error(error: DatabaseError):
        app.logger.error("database error: %s", error)
        return error_response("service_unavailable", "The service is temporarily unavailable.", 503)

    @app.errorhandler(Exception)
    def unexpected_error(error: Exception):
        app.logger.exception("unexpected application error")
        return error_response("internal_error", "An unexpected error occurred.", 500)
