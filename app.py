"""Thin local development entry point; importing it does not start a server."""

from sentinal.api import create_app
from sentinal.config import Settings

app = create_app()


def main() -> None:
    settings = Settings.from_env()
    app.run(host=settings.host, port=settings.port, debug=settings.debug)


if __name__ == "__main__":
    main()
