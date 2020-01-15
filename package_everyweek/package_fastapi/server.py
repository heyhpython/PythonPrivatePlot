# coding=utf-8
# builtins
# third party package
from fastapi import FastAPI
from pydantic import BaseModel
# self built

app = FastAPI()
# uvicorn server:app --host 0.0.0.0 --reload


class User(BaseModel):
    name: str
    salary: float
    married: bool


@app.get("/")
def index():
    return {"hello": "world"}


@app.get("/users/{user_id}")
def get_user(user_id: int, q: str=None):
    return {"user_id": user_id, "q": q}


@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    return {"name": user.name, "married": user.married}