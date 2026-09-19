"""Domain exceptions safe to map at the API boundary."""


class SentinalError(Exception):
    """Base application exception."""


class ConfigurationError(SentinalError):
    """Raised when configuration is malformed or unsafe."""


class DatabaseError(SentinalError):
    """Raised when the local database cannot be safely used."""


class ApplicationError(SentinalError):
    """An expected application error suitable for a client response."""

    def __init__(
        self, message: str, status_code: int = 503, code: str = "service_unavailable"
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
