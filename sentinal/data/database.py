"""Minimal SQLite ownership abstraction for application metadata only."""

import sqlite3
from pathlib import Path

from sentinal.core.exceptions import DatabaseError


class Database:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._connection: sqlite3.Connection | None = None

    def initialize(self) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self._connection = sqlite3.connect(self.path)
            self._connection.execute(
                "CREATE TABLE IF NOT EXISTS app_metadata "
                "(key TEXT PRIMARY KEY, value TEXT NOT NULL)"
            )
            self._connection.execute(
                "INSERT OR IGNORE INTO app_metadata (key, value) VALUES "
                "('schema_version', '1')"
            )
            self._connection.commit()
        except (OSError, sqlite3.Error) as exc:
            self.close()
            raise DatabaseError("The application database could not be initialized.") from exc

    def connection(self) -> sqlite3.Connection:
        if self._connection is None:
            raise DatabaseError("The application database is not initialized.")
        return self._connection

    def health(self) -> bool:
        try:
            self.connection().execute("SELECT 1").fetchone()
            return True
        except (DatabaseError, sqlite3.Error):
            return False

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None
