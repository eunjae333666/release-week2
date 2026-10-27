# 2주차 FastAPI 실습

이름을 받아 인사말을 반환하는 작은 API다. `uv`로 의존성을 관리하고, `src/` 레이아웃과 `uv_build` 빌드 백엔드를 사용한다.

## 파일 구성

| 파일 | 역할 |
| --- | --- |
| `backend/src/backend/main.py` | FastAPI 앱, 인사 함수, 요청 모델 |
| `backend/tests/test_main.py` | 정상 입력과 빈 문자열 입력 테스트 |
| `backend/pyproject.toml` | 프로젝트 정보, 의존성, 빌드 설정 |
| `backend/uv.lock` | 의존성 버전 기록 |
| `backend/.python-version` | 사용할 Python 버전 |
| `.pre-commit-config.yaml` | 커밋 전 파일 검사 설정 |

강의의 `main.py`는 `backend/src/backend/main.py`로 옮겼다. 테스트는 `backend/tests/test_main.py`에 있으며, 앱을 불러오는 코드는 `from backend.main import app`이다. API 기능과 두 테스트의 내용은 강의 예제와 같다.

## 실행

`uv`를 설치한 뒤 저장소의 루트 폴더에서 아래 명령을 한 줄씩 실행한다. `uv sync`는 저장된 프로젝트 설정과 잠금 파일을 이용해 Python 환경과 의존성을 준비한다.

```bash
cd backend
uv sync
uv run pre-commit install
uv run fastapi dev src/backend/main.py
```

`pre-commit install`은 이 저장소에 커밋 전 검사 훅을 등록한다. 저장소를 새로 받은 사람은 각자 한 번 실행한다.

서버가 실행 중인 상태에서 브라우저로 [API 문서](http://127.0.0.1:8000/docs)를 연다. 이후 명령도 `backend` 폴더에서 실행한다.

## API 확인

| 메서드 | 경로 | 동작 |
| --- | --- | --- |
| GET | `/health` | `{"status": "ok"}` 반환 |
| GET | `/hello?name=민수` | 쿼리 파라미터의 이름으로 인사말 반환. 이름을 생략하면 `친구` 사용 |
| POST | `/hello` | JSON 본문의 이름을 검증한 뒤 인사말 반환 |

POST 요청은 `/docs`에서 `POST /hello`를 선택하고 **Try it out**을 누른 뒤, 다음 본문을 입력하고 **Execute**를 누른다.

```json
{"name": "민수"}
```

정상 요청에는 상태 코드 `200`과 다음 응답을 반환한다.

```json
{"message": "안녕하세요, 민수님!"}
```

POST의 `name`은 필수 문자열이며 길이는 1~30자다. `{}`처럼 이름을 생략하거나 `{"name": ""}`처럼 빈 문자열을 보내면 상태 코드 `422`를 반환한다.

## 테스트

서버를 실행한 터미널에서 `Ctrl+C`로 종료한 뒤 실행한다. `TestClient` 테스트에는 실행 중인 서버가 필요 없다.

```bash
uv run pytest
```

정상 요청의 인사말과 빈 문자열 요청의 오류 응답을 확인하는 두 테스트가 있다.

## pre-commit 검사

Git 강의와 같은 세 가지 훅을 사용한다.

- `trailing-whitespace`: 줄 끝 공백 제거
- `end-of-file-fixer`: 파일 끝 개행 정리
- `check-yaml`: YAML 문법 검사

전체 파일을 직접 검사하려면 다음 명령을 실행한다.

```bash
uv run pre-commit run --all-files
```

훅이 파일을 수정하면 변경 내용을 확인하고 `git add`한 뒤 다시 커밋한다.

## 빌드

```bash
uv build
```

`uv_build`가 패키지를 빌드하며, 결과 파일은 `backend/dist/`에 생성된다.

## 참고 문서

- [uv 설치](https://docs.astral.sh/uv/getting-started/installation/)
- [uv 빌드 백엔드](https://docs.astral.sh/uv/concepts/build-backend/)
- [pre-commit](https://pre-commit.com/)
