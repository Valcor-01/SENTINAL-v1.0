# Development

## Setup

Use Python 3.11+ and create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

Run `python app.py` for local development. The server starts only when the entry point is run, not when the factory is imported.

## Validation

```powershell
python -m pytest
ruff check .
python -m build
pip-audit
```

The local database is intentionally disposable development state under `data/` by default and is ignored by Git. Do not put secrets in `.env` or logs.
