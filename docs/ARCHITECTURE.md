# Architecture

## Implemented foundation

```text
SENTINAL
  └─ Flask application factory
      ├─ validated configuration
      ├─ lifecycle and structured logging
      ├─ API layer
      │   └─ GET /api/health
      └─ SQLite data layer
          └─ app_metadata only
```

`app.py` is a thin local entry point. `sentinal.api.create_app()` wires settings, logging, the database, lifecycle, request IDs, errors, and routes without starting a server. The lifecycle owns database shutdown. The data layer owns the only SQLite connection and creates no event or telemetry tables.

## Planned

System Intelligence, telemetry models, event storage, monitoring components, security analysis, AI, dashboard, and all non-Python components are planned and intentionally absent.
