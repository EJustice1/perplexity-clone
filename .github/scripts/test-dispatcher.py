import os
import pytest
import requests

DISPATCHER_URL = os.environ.get("DISPATCHER_URL")
if not DISPATCHER_URL:
    raise RuntimeError("DISPATCHER_URL environment variable must be set")

ENDPOINT = DISPATCHER_URL.rstrip("/") + "/dispatcher/dispatch"


def test_dispatcher_returns_204():
    response = requests.post(ENDPOINT, timeout=30)
    assert response.status_code == 204, f"Expected 204, got {response.status_code}: {response.text}"
