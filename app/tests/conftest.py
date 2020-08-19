"""
Pytest Fixtures
"""

import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client():
    """
    Test client fixture.
    """
    client = TestClient(app)
    yield client  # testing happens here
