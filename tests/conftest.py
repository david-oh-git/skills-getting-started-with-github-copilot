from fastapi.testclient import TestClient
import copy

import pytest

from src.app import app, activities as activities_data


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(activities_data)
    yield
    activities_data.clear()
    activities_data.update(original)


@pytest.fixture
def client():
    return TestClient(app)
