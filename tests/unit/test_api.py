import pytest
from unittest.mock import patch

from api.app import app as flask_app


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    return flask_app.test_client()


def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'


def test_get_metrics_empty(client):
    response = client.get('/api/metrics')
    assert response.status_code == 200
    assert response.get_json() == {}


def test_get_metrics_for_specific_host(client):
    from api.app import set_metrics
    set_metrics("192.168.1.10", {
        "host": "192.168.1.10",
        "hostname": "test-server",
        "cpu_used_pct": 45.5,
        "ram": {"total_mb": 16384, "used_mb": 8192, "used_pct": 50.0},
        "interfaces": {}
    })
    response = client.get('/api/metrics/192.168.1.10')
    assert response.status_code == 200
    assert response.get_json()["cpu_used_pct"] == 45.5


@patch('api.app._metrics', new_callable=dict)
def test_get_metrics_host_not_found(mock_metrics, client):
    response = client.get('/api/metrics/999.999.999.999')
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Host not found'