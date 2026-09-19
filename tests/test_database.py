import pytest

from sentinal.core.exceptions import DatabaseError
from sentinal.data import Database


def test_database_initializes_metadata_and_health(tmp_path) -> None:
    database = Database(tmp_path / "state.db")
    database.initialize()
    assert database.health() is True
    version = database.connection().execute(
        "SELECT value FROM app_metadata WHERE key = 'schema_version'"
    ).fetchone()
    assert version == ("1",)
    database.close()
    assert database.health() is False


def test_invalid_database_path_raises_safe_error(tmp_path) -> None:
    blocking_file = tmp_path / "not-a-directory"
    blocking_file.write_text("blocked", encoding="utf-8")
    with pytest.raises(DatabaseError, match="could not be initialized"):
        Database(blocking_file / "state.db").initialize()
