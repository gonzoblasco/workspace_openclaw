from fastapi.testclient import TestClient

from src.agent.ui import app


def test_get_root():
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    assert "<html" in resp.text.lower()


def test_health():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "ollama_ok" in data


def test_delete():
    client = TestClient(app)
    resp = client.post("/delete")
    assert resp.status_code == 204
