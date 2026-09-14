from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_process():
    response = client.post(
        "/process",
        json={"events": [{"device_id": "d1", "value": 1.5}]},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["events"] == 1
    assert body["throughput_events_per_second"] > 0
