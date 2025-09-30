import os

import pytest
import requests

WORKER_URL = os.environ.get("WORKER_URL")


@pytest.mark.skip(reason="Worker functionality not yet implemented")
def test_worker_placeholder_dispatcher_trigger():
    if not WORKER_URL:
        pytest.skip("WORKER_URL not configured")

    response = requests.post(WORKER_URL.rstrip("/") + "/dispatcher/dispatch", timeout=30)
    assert response.status_code in {200, 204}
