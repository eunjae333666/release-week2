from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_hello_post():
    response = client.post("/hello", json={"name": "민수"})
    assert response.status_code == 200
    assert response.json() == {"message": "안녕하세요, 민수님!"}


def test_hello_empty_name():
    response = client.post("/hello", json={"name": ""})
    assert response.status_code == 422
