import pytest
from fastapi.testclient import TestClient

from file_converter.routes.base import app


@pytest.fixture
def client():
    client = TestClient(app)
    return client
