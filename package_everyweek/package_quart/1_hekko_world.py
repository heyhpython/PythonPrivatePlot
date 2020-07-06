# coding=utf-8
# builtins
# third party package
from quart import Quart, websocket
# self built


app = Quart(__name__)


@app.route('/')
async def hello():
    return {"hello": "world"}


@app.websocket('/ws')
async def wd():
    while 1:
        await websocket.send('hello')


if __name__ == "__main__":
    app.run()
