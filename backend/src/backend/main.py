from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


def greet(name: str) -> str:
    return f"안녕하세요, {name}님!"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/hello")
def hello(name: str = "친구"):
    return {"message": greet(name)}


class HelloRequest(BaseModel):
    name: str = Field(min_length=1, max_length=30)


@app.post("/hello")
def hello_post(body: HelloRequest):
    return {"message": greet(body.name)}
