import pytest
from api.app import app as flask_app


@pytest.fixture(scope="session")
def app():
    flask_app.config.update({
        "TESTING": True,
        "DEBUG": False,
    })
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()