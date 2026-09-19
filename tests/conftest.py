from pathlib import Path

import pytest

from sentinal.api import create_app
from sentinal.config import Settings


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(
        environment="testing",
        host="127.0.0.1",
        port=8000,
        debug=False,
        database_path=tmp_path / "sentinal.db",
        log_level="INFO",
    )


@pytest.fixture
def app(settings: Settings):
    application = create_app(settings)
    yield application
    application.extensions["sentinal_lifecycle"].shutdown()


@pytest.fixture
def client(app):
    return app.test_client()
