import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
from pathlib import Path
import sys

# Ensure src is importable from tests.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Create a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activity database before each test."""
    original_state = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_state)
