# FastAPI 백엔드

2주차 강의의 인사 API 예제다. `uv`로 의존성을 관리하고, `src/backend`에 코드를 둔다.
빌드 백엔드는 `uv_build`다.

이 폴더에서 실행한다.

```bash
uv sync
uv run fastapi dev src/backend/main.py
```

브라우저에서 <http://127.0.0.1:8000/docs>를 연다.
서버를 `Ctrl+C`로 종료한 뒤 테스트와 빌드를 실행할 수 있다.

```bash
uv run pytest
uv build
```

pre-commit 설정과 전체 실행 순서는 [저장소 README](../README.md)를 참고한다.
