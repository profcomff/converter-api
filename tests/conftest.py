import pytest
from fastapi.testclient import TestClient
from file_converter.routes.base import app


@pytest.fixture(scope='session')
def client():
    client = TestClient(app)
    return client
