# API Documentation

## `GET /api/health`

Returns readiness of the Flask application, lifecycle, and local SQLite connection. It does not report operating-system or telemetry health.

```json
{"data":{"status":"healthy","version":"0.1.0"},"meta":{"service":"sentinal"}}
```

Every response includes `X-Request-ID`. A safe incoming value is accepted; otherwise the service generates one. Errors use `error.code`, `error.message`, and `error.request_id` and do not expose stack traces, paths, configuration, or secrets.

Authentication, versioning, telemetry APIs, and state-changing routes are **PLANNED** and not implemented.
