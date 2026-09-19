"""SENTINAL application package."""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def _project_version() -> str:
    """Expose the installed package version, with a source-tree fallback."""
    try:
        return version("sentinal")
    except PackageNotFoundError:
        import tomllib

        project_file = Path(__file__).resolve().parent.parent / "pyproject.toml"
        return tomllib.loads(project_file.read_text(encoding="utf-8"))["project"]["version"]


__version__ = _project_version()
