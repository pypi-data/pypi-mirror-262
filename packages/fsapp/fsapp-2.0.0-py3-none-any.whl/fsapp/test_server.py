from fastapi.testclient import TestClient
from fsapp.base import app
from fsapp.core.config import settings

client = TestClient(app)


def test_main_page():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': f"Hello {settings.required.instance}"}


def test_security():
    login_data = {
        "grant_type": "",
        "username": "qwe",
        "password": "qwe",
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }
    response = client.post('/auth/token', data=login_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect username or password"}


def test_search_response_unauthorized():
    response = client.post('/api/v1/search', data={})
    assert response.status_code == 401
