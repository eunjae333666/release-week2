# SI Unit Decomposer

SI 유도 단위를 SI 기본 단위로 분해하는 웹 애플리케이션입니다.

사용자가 단위 수식을 입력하면 FastAPI 백엔드에서 차원을 분석하고, React 프론트엔드에서 결과를 표시합니다.

## 기술 스택

- **Backend:** Python, FastAPI, Pydantic
- **Frontend:** React, JavaScript, Vite
- **Testing:** pytest, FastAPI TestClient
- **Package Management:** uv, npm
- **Web Server:** Nginx
- **Containerization:** Docker, Docker Compose

## 주요 기능

- SI 기본 단위 및 이름이 붙은 SI 유도 단위 분석
- 곱셈(`*`), 나눗셈(`/`), 정수 거듭제곱(`^`) 지원
- 같은 단위가 여러 번 등장하는 수식 처리
- 차원이 소거되면 `1` 출력
- 잘못된 입력에 대한 오류 메시지 표시

### 사용 예시

| 입력 | 출력 |
|---|---|
| `N` | `kg·m·s⁻²` |
| `N*m` | `kg·m²·s⁻²` |
| `N/m^2` | `kg·m⁻¹·s⁻²` |
| `N^2/N` | `kg·m·s⁻²` |
| `s/s` | `1` |

괄호와 단위의 크기 변환 계수는 지원하지 않습니다.

## 프로젝트 구조

```
week2/
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── README.md
│   ├── src/
│   │   └── backend/
│   │       ├── __init__.py
│   │       ├── main.py
│   │       └── analyzer.py
│   └── tests/
│       └── test_main.py
│
├── frontend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── nginx.conf
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── compose.yaml
├── .gitignore
└── README.md
```

## Docker Compose 실행 (3주차)

Docker를 이용해 프론트엔드와 백엔드를 각각 컨테이너로 실행하고, Docker Compose로 통합 관리합니다.

### 실행 환경

- Docker Desktop (또는 Docker Engine)
- Docker Compose

### 실행

프로젝트 최상위 디렉터리에서 다음 명령어를 실행합니다.

```bash
docker compose up --build -d
```

브라우저에서 `http://localhost:8080`으로 접속합니다.

### 실행 상태 확인

```bash
docker compose ps
```

백엔드의 healthcheck를 통해 정상 실행 여부를 확인할 수 있습니다.

로그 확인:

```bash
docker compose logs -f
```

### 종료

```bash
docker compose down
```

### 컨테이너 구성

- **Backend:** Python 3.12와 FastAPI를 사용하며, Uvicorn으로 API 서버를 실행합니다.
- **Frontend:** Node.js로 React 애플리케이션을 빌드한 후 Nginx를 통해 정적 파일을 제공합니다.
- **Nginx:** `/api/`로 시작하는 요청을 백엔드 컨테이너로 전달하면서 `/api/` 접두사를 제거합니다.
- **Docker Compose:** 두 서비스의 빌드, 네트워크 연결, 포트 매핑 및 백엔드 healthcheck를 관리합니다.

브라우저의 `/api/analyze` 요청은 Nginx를 거쳐 FastAPI의 `/analyze` 엔드포인트로 전달됩니다.

별도의 데이터베이스를 사용하지 않으므로 영구 데이터 저장용 Docker Volume은 구성하지 않았습니다.


## 실행 방법

### 1. 백엔드

```bash
cd backend
uv sync
uv run fastapi dev src/backend/main.py
```

백엔드 API 문서는 다음 주소에서 확인할 수 있습니다.

`http://127.0.0.1:8000/docs`

### 2. 프론트엔드

별도의 터미널에서 실행합니다.

```bash
cd frontend
npm install
npm run dev
```

터미널에 표시되는 로컬 주소(일반적으로 `http://localhost:5173`)로 접속합니다.

백엔드와 프론트엔드는 동시에 실행되어야 합니다.

## API

### POST /analyze

**요청**

```json
{
  "input": "N*m/s^2"
}
```

**응답**

```json
{
  "result": "kg·m²·s⁻⁴"
}
```

잘못된 단위 또는 수식은 HTTP 400 오류로 처리합니다. 입력 길이 제한 등 Pydantic 검증 오류는 HTTP 422로 처리됩니다.

## 테스트

백엔드 디렉터리에서 다음 명령어를 실행합니다.

```bash
uv run pytest
```

정상적인 단위 분해, 반복되는 단위, 무차원 결과, 잘못된 입력 등을 테스트합니다.

## 프론트엔드 정적 빌드

```bash
cd frontend
npm run build
```

빌드 결과물은 `frontend/dist/`에 생성됩니다.
