import pytest
import json

def test_app(client):
    assert client.get('accounts/accounts').status_code == 200

def test_post_account(client):

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
            "account_id": 9999,
            "type": "checking",
            "name": "testing",
            "birthdate": "1985-06-06",
            "phone": "55511123111",
            "email": "email@test.com",
            "balance": 0
    }

    url = 'accounts/accounts'

    response = client.post(url, data=json.dumps(data), headers=headers)
    
    assert response.status_code == 201
    #assert response.content_type == mimetype
    #assert response.json['Result'] == 39