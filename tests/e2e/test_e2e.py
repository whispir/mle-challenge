import json
import os

import pytest
from fastapi.testclient import TestClient

from windml.app import app

client = TestClient(app)


TEST_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(TEST_ROOT)


@pytest.fixture
def event_01():
    with open(os.path.join(TEST_ROOT, 'events/event.test.01.json')) as jf:
        data = json.load(jf)
    return data


class TestAPI:
    def test_health_check(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_event_01(self, event_01):
        response = client.post("/estimate", json=event_01)
        assert response.status_code == 200


