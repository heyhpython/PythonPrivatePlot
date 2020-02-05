# coding=utf-8
# builtins
import time
# third party package
from fastapi import FastAPI, Path, Query, Body, File, UploadFile, Depends
from pydantic import BaseModel as BM, Field, HttpUrl, BaseConfig as BG
from starlette.responses import JSONResponse
from starlette.requests import Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# self built

app = FastAPI()
# uvicorn server:app --host 0.0.0.0 --reload
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# class BaseConfig(BM):
#     orm_mode: bool = True
#
#
# class BaseModel(BM):
#     Config = BaseConfig
#     __config__ = BaseConfig


class User(BM):
    name: str
    salary: float
    married: bool


@app.get("/")
def index():
    return {"hello": "world"}


@app.put("/users/{user_id}")
def update_user(user_id: int, user: User, q=None):
    return {"name": user.name, "married": user.married, "q":q}


@app.get("/users")
def update_user(token: str=Depends(oauth2_scheme)):
    return {"token": token}


@app.post("/token")
def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": f"{form_data.username}-{form_data.password}", "token_type": "bearer"}


@app.middleware("http")
async def after_request(req: Request, call_nxt):
    start_time = time.time()
    response = await call_nxt(req)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)