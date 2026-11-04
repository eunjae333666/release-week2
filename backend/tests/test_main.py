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


# 정상적인 SI 단위 변환
def test_analyze_newton():
    response = client.post("/analyze", json={"input": "N"})

    assert response.status_code == 200
    assert response.json() == {
        "result": "kg·m·s⁻²"
    }


# 곱셈과 나눗셈
def test_analyze_expression():
    response = client.post("/analyze", json={"input": "N*m/s^2"})

    assert response.status_code == 200
    assert response.json() == {
        "result": "kg·m²·s⁻⁴"
    }


# 같은 단위가 반복되는 경우
def test_analyze_repeated_unit():
    response = client.post("/analyze", json={"input": "N^2/N"})

    assert response.status_code == 200
    assert response.json() == {
        "result": "kg·m·s⁻²"
    }


# 차원이 모두 소거되는 경우
def test_analyze_dimensionless():
    response = client.post("/analyze", json={"input": "N/N"})

    assert response.status_code == 200
    assert response.json() == {
        "result": "1"
    }


# 지원하지 않는 단위
def test_analyze_unknown_unit():
    response = client.post("/analyze", json={"input": "abc"})

    assert response.status_code == 400


# 빈 문자열 (Pydantic 검증)
def test_analyze_empty_input():
    response = client.post("/analyze", json={"input": ""})

    assert response.status_code == 422


# 입력 길이 초과 (Pydantic 검증)
def test_analyze_too_long():
    response = client.post("/analyze", json={"input": "N" * 31})

    assert response.status_code == 422


# 필수 필드 누락
def test_analyze_missing_input():
    response = client.post("/analyze", json={})

    assert response.status_code == 422
