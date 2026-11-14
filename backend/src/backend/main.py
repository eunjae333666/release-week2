
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from backend.analyzer import analyze

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


# 기존 예제 API
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


#SI unit analyze
class AnalyzeRequest(BaseModel):
    input: str=Field(min_length=1,max_length=30)



@app.post("/analyze")
def analyze_post(body: AnalyzeRequest):
    try:
        return {"result": analyze(body.input)}

    except ValueError as error:
        raise HTTPException(status_code=400,detail=str(error)) from error
