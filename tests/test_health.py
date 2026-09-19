def test_health_endpoint_reports_application_readiness(client) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {
        "data": {"status": "healthy", "version": "0.1.0"},
        "meta": {"service": "sentinal"},
    }
    assert response.headers["X-Request-ID"]


def test_health_accepts_safe_request_id(client) -> None:
    response = client.get("/api/health", headers={"X-Request-ID": "audit-123"})
    assert response.headers["X-Request-ID"] == "audit-123"


def test_not_found_and_method_errors_are_structured(client) -> None:
    responses = (
        (client.get("/missing"), "not_found"),
        (client.post("/api/health"), "method_not_allowed"),
    )
    for response, code in responses:
        body = response.get_json()
        assert body["error"]["code"] == code
        assert body["error"]["request_id"] == response.headers["X-Request-ID"]
        assert body["meta"] == {"service": "sentinal"}


def test_shutdown_makes_health_unavailable(settings) -> None:
    application = create_app(settings)
    application.extensions["sentinal_lifecycle"].shutdown()
    response = application.test_client().get("/api/health")
    assert response.status_code == 503
    assert response.get_json()["error"]["code"] == "service_unavailable"
