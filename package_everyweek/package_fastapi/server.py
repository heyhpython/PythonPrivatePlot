# coding=utf-8
# builtins
# third party package
from fastapi import FastAPI, Path, Query, Body, File, UploadFile
from pydantic import BaseModel as BM, Field, HttpUrl, BaseConfig as BG
from starlette.responses import JSONResponse
from starlette.requests import Request
# self built

app = FastAPI()
# uvicorn server:app --host 0.0.0.0 --reload


class BaseConfig(BM):
    orm_mode: bool = True


class BaseModel(BM):
    Config = BaseConfig
    __config__ = BaseConfig


class User(BaseModel):
    name: str
    salary: float
    married: bool


@app.get("/")
def index():
    return {"hello": "world"}


@app.put("/users/{user_id}")
def update_user(user_id: int, user: User, q=None):
    return {"name": user.name, "married": user.married, "q":q}
