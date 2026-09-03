from fastapi.testclient import TestClient

from ai_ta_api.main import app

client = TestClient(app)


def test_health_return_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "env": "local", "version": app.version}

def test_health_reports_env(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "env": "test", "version": app.version}
