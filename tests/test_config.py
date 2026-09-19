from pathlib import Path

import pytest

from sentinal.config import Settings
from sentinal.core.exceptions import ConfigurationError


def test_default_configuration() -> None:
    settings = Settings.from_env({})
    assert settings.environment == "production"
    assert settings.host == "127.0.0.1"
    assert settings.port == 8000
    assert settings.debug is False
    assert settings.database_path == Path("data/sentinal.db")


def test_environment_overrides() -> None:
    settings = Settings.from_env(
        {
            "SENTINAL_ENV": "testing",
            "HOST": "0.0.0.0",
            "PORT": "9000",
            "DEBUG": "true",
            "DATABASE_PATH": "custom.db",
            "LOG_LEVEL": "debug",
        }
    )
    assert settings.environment == "testing"
    assert settings.port == 9000
    assert settings.debug is True
    assert settings.log_level == "DEBUG"


@pytest.mark.parametrize(
    ("key", "value"),
    [("PORT", "invalid"), ("PORT", "0"), ("DEBUG", "sometimes"), ("LOG_LEVEL", "verbose")],
)
def test_invalid_configuration_is_rejected(key: str, value: str) -> None:
    with pytest.raises(ConfigurationError):
        Settings.from_env({key: value})


def test_dotenv_file_is_loaded_without_overriding_environment(tmp_path, monkeypatch) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("PORT=9001\nDEBUG=true\n", encoding="utf-8")
    monkeypatch.delenv("PORT", raising=False)
    monkeypatch.delenv("DEBUG", raising=False)
    settings = Settings.from_env(dotenv_path=env_file)
    assert settings.port == 9001
    assert settings.debug is True
