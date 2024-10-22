import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    # Setup: create a TestClient instance
    with TestClient(app) as client:
        yield client  # This is where the testing happens
