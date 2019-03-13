import pytest

def test_app(client):
    assert client.get('accounts/accounts').status_code == 200