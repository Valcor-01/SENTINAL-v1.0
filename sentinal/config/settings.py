"""Validated application settings loaded from the environment."""

from dataclasses import dataclass
from os import environ
from pathlib import Path
from typing import Mapping

from dotenv import load_dotenv

from sentinal.core.exceptions import ConfigurationError

_TRUE_VALUES = {"1", "true", "yes", "on"}
_FALSE_VALUES = {"0", "false", "no", "off"}
_VALID_LOG_LEVELS = {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"}


@dataclass(frozen=True, slots=True)
class Settings:
    environment: str
    host: str
    port: int
    debug: bool
    database_path: Path
    log_level: str

    @classmethod
    def from_env(
        cls,
        values: Mapping[str, str] | None = None,
        dotenv_path: str | Path | None = None,
    ) -> "Settings":
        if values is None:
            load_dotenv(dotenv_path=dotenv_path, override=False)
            values = environ

        environment = values.get("SENTINAL_ENV", "production").strip().lower()
        if environment not in {"development", "production", "testing"}:
            raise ConfigurationError("SENTINAL_ENV must be development, production, or testing.")

        host = values.get("HOST", "127.0.0.1").strip()
        if not host:
            raise ConfigurationError("HOST must not be empty.")

        port = _parse_port(values.get("PORT", "8000"))
        debug = _parse_bool(values.get("DEBUG", "false"), "DEBUG")
        log_level = values.get("LOG_LEVEL", "INFO").strip().upper()
        if log_level not in _VALID_LOG_LEVELS:
            raise ConfigurationError(
                "LOG_LEVEL must be one of CRITICAL, ERROR, WARNING, INFO, or DEBUG."
            )

        database_value = values.get("DATABASE_PATH", "data/sentinal.db").strip()
        if not database_value:
            raise ConfigurationError("DATABASE_PATH must not be empty.")

        return cls(environment, host, port, debug, Path(database_value), log_level)


def _parse_port(raw_value: str) -> int:
    try:
        port = int(raw_value)
    except ValueError as exc:
        raise ConfigurationError("PORT must be an integer between 1 and 65535.") from exc
    if not 1 <= port <= 65535:
        raise ConfigurationError("PORT must be an integer between 1 and 65535.")
    return port


def _parse_bool(raw_value: str, name: str) -> bool:
    value = raw_value.strip().lower()
    if value in _TRUE_VALUES:
        return True
    if value in _FALSE_VALUES:
        return False
    raise ConfigurationError(f"{name} must be a boolean value.")
