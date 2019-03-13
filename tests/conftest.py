import sys
sys.path.append('./api/')
import pytest
import run

@pytest.fixture
def client():
    run.app.config['TESTING'] = True
    client = run.app.test_client()

    yield client
