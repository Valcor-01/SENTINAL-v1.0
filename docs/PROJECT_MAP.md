# Project Map

| Requirement | Architecture | Module/language | API | Tests | Documentation |
| --- | --- | --- | --- | --- | --- |
| Application composition | Flask factory | `sentinal/api/app.py` / Python | `GET /api/health` | `test_health.py` | ARCHITECTURE, API |
| Configuration | Typed settings | `sentinal/config/settings.py` / Python | N/A | `test_config.py` | DEVELOPMENT |
| Lifecycle and logging | Core | `sentinal/core/` / Python | Request IDs | `test_lifecycle.py` | ARCHITECTURE |
| Local metadata storage | SQLite abstraction | `sentinal/data/database.py` / Python | Readiness only | `test_database.py` | ARCHITECTURE |
| System telemetry | Component layer | PLANNED | Not implemented | Not implemented | ROADMAP |
| Security observations | Security engine | Not implemented | Not implemented | Not implemented | SECURITY |
| Event normalization | Event model | Not implemented | Not implemented | Not implemented | ROADMAP |
| Dashboard | TypeScript UI | PLANNED | Not implemented | Not implemented | README |

This map must be updated as requirements become architecture decisions, modules, APIs, tests, and user documentation.
