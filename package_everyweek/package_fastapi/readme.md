## FastAPI 学习笔记
- [项目github地址](https://github.com/tiangolo/fastapi)
- [官方文档](https://fastapi.tiangolo.com/)

### hello world

```python
# 导入包
from fastapi import FastAPI
# 创建一个应用
app = FastAPI()
# 注册路由

@app.get("/")  
def index():
    return {"hello": "world"}
```
- get表示请求方式 , 还可是post, patch, delete...
- 第一个位置参数表示的是请求的路径
- 返回一个python的字典会被框架转化为json返回给客户端, 可以返回一个pydantic model 甚至ORM model
- 路由函数可以使用async def:... 这样的async/await模式

### 如何启动web服务
```shell script
pip install uvicorn  # 只用执行一次
uvicorn server:app --host 0.0.0.0 --reload
```
- FastAPI没有实现SGI， 所以还需要异步网关协议接口(ASGI)服务器

### 基本参数解析
```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    salary: float
    married: bool

@app.get("/users/{user_id}")
def get_user(user_id: int, user:User, q: str=None):
    return {"name": user.name, "married": user.married, "q":q}
```
- [参数定义](https://fastapi.tiangolo.com/tutorial/body/)
- 路径里的user_id参数将会被解析并传参给路由函数
- 如果参数定义的是值类型如：int，str， bool等，将作为请求参数如例子里
- BaseModel类型的参数将从body里解析，传给路由函数
- BaseModel的属性如果规定了类型的话，会进行类型校验, 给了默认值则是为可选，否则是必须
- 参数类型可以是枚举类型， 如下
```python
from enum import Enum
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
@app.get("/users/{user_id}")
def get_user(user_id: int, user:User, q: ModelName=None):
    return {"name": user.name, "married": user.married, "q":q}
```
### 参数校验器
```python
from fastapi import Path, Query, Body
@app.get("/users/{user_id}")
def get_user(user_id: int = Path(...), user:User = Body(...), q: str=Query(None, max_length=50, min_length=3)):
    return {"name": user.name, "married": user.married, "q":q}
```
- 参数q的值类型与q:str=None一致，但是当长度超出max_length或小于min_length是会校验失败
- 当q是必须要的参数时None为str=Query(...)
- 当q为多值是q:sList[str] = Query(["a", "b"])  类似于flask_restful的参数解析里的append行为
- 更多可选项![参数](https://github.com/heyhpython/PythonPrivatePlot/blob/master/package_everyweek/package_fastapi/paras.png)
- Body类型的参数可以传多个，甚至可以传值类型的参数，传值类型时，必须指定为Body[body参数](https://fastapi.tiangolo.com/tutorial/body-multiple-params/)
- Body, Path, Query等是pydantic.FieldInfo的封装 功能与其一致， 可以使用在data model里作为校验。 如下
- Body 可以添加传example参数， 用于给文档显示传参范例， example的值为dict
- BaseModel的字段类型可以支持多种类型，甚至于自定义类型（实现了validate的类方法）,见[复杂参数解析](https://fastapi.tiangolo.com/tutorial/body-nested-models/ )
```python
from pydantic import Field, BaseModel
    
class User(BaseModel):
    name: str = Field(..., max_length=50)
    salary: float 
    married: bool
```
### Cookie, Header 
```python
from fastapi import Cookie, Header
@app.get("/")
async def read_items(*, user_agent: str = Header(None), token: str = Cookie(None)):
    return {"User-Agent": user_agent}

```
- str类型可以是修改为自定义的BaseModel子类， 然后自定义TokenFiled 并实现validate方法
- fastapi会将'_'自动转化为'-'，并且无视大小写， 若特殊要求不转化，设置参数`convert_underscores=False`
### Response
```python
from typing import List
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    tags: List[str] = []


@app.post("/items/", response_model=Item, response_model_include={"name", "price"}, 
            resresponse_model_exclude={"tax"}, response_model_exclude_unset=True)
async def create_item(item: Item):
    return item

```
- response_model参数会对返回值进行验证，并转化为json格式，以及在自动生成的文档中被使用
- 如果路由函数返回了超出return_model字段的对象， fastapi会自动删除不属于return_model的字段
- response_model_include or response_model_exclude 参数会决定哪些字段被返回，但是不会影响文档
- response_model_exclude_unset会派出未给值的字段，包括已经设置默认值的
- [更多返回值的特性](https://fastapi.tiangolo.com/tutorial/extra-models/)
- 可以根据路由函数不同的处理条件，返回不同的状态码 [详情](https://fastapi.tiangolo.com/tutorial/additional-status-codes/)
- 可自定义返回相应类型， fastapi会直接返回该响应，[详情](https://fastapi.tiangolo.com/tutorial/custom-response/)

### http状态码
```python
@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}
```
- 当路由函数正常返回时， 201将作为状态码返回
- 更多状态码在starlette.status

### 错误处理
```python
from fastapi import FastAPI, HTTPException

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    raise HTTPException(
                status_code=404,
                detail="Item not found",
                headers={"X-Error": "There goes my error"},
             ) 
```
- HTTPEXception会返回给客户端一个指定状态码及响应头的响应
- fastapi的错误处理来自于starlette，使用方法与starlette一致
- 为处理代码错误， fastapi支持针对不同的错误类型注册全局错误处理如下
```python
from starlette.requests import Request
from starlette.responses import JSONResponse
@app.exceptiom_handler(Exception)
async def exec_handler(request:Request, exc: Exception):
    return JSONResponse(
        status_code=419,
        content={"message": str(Exception)}
    )
```

### 响应的Cookie&Header
```python
from starlette.responses import JSONResponse, Response

@app.get("/user1")
def get_user1():
    content = {"message": "Hello World"}
    headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)

@app.get("/user2")
def get_user2(response: Response):
    content = {"message": "Hello World"}
    response.headers.update({"X-Cat-Dog": "alone in the world"})
    response.set_cookie(key="cookie", value="this is a cookie")
    return content
``` 
- 自定义的响应头需要以`X-`开头

### 安全性Security
- fastapi的security模块提供快速搭建用户验证及鉴权的方案
```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": hash(form_data.username), "token_type": "bearer"}
    
@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```
- tokenUrl指明了生成token的url，但是并没有实现验证账户密码及生成token的逻辑，需要使用者自己实现
- 调用api时不符合OAuth2 Bearer规范的token将会直接返回401未授权
- login接口的返回值必须包含access_token和token_type两个字段

### 中间件(类似flask请求钩子)
```python
@app.middleware("http")
def after_request(req: Request, call_nxt):
    start_time = time.time()
    response = await call_nxt(req)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```
- 可以添加错误处理的中间件或者响应加密、压缩等

### 跨域资源共享(CORS)
```python
from starlette.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # can be ["*"]
    allow_credentials=True,
    allow_methods=["*"],  # allow all method
    allow_headers=["*"],  # allow all header
)
```
### APIRouter(flask blueprint)
- file user

```python
from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["users"])
async def read_users():
    return [{"username": "Foo"}, {"username": "Bar"}]
    
app.include_router(
    router,
    prefix="/users",
    tags=["items"],
    #dependencies=[Depends(get_token_header)],
    )
```
- 使用include_router注册路由
- 使用preifix参数给路由添加路径前缀
- 使用dependencies参数给该路由下的所有处理函数注入依赖

### background task
```python
from fastapi import BackgroundTasks

def execute_background():
    # some thing need tobe execute after return response
    pass

@app.post("/send-notification/{email}")
async def send_notification(background_tasks: BackgroundTasks):
    background_tasks.add_task(execute_background)
    return {"message": "operations will execute backgroud"}
```
- execute_background会在返回响应之后在后台执行
- 后台任务用法适用于计算量小的，需要共享内存的场景
- 当需要执行大量且计算量大，或者在新的进程中执行时，可以使用celery[模板](https://fastapi.tiangolo.com/project-generation/) 

### 静态文件
```bash pip install aiofiles
```
```python
from starlette.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
```

### 测试
```python
from starlette.testclient import TestClient
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```
- 可以使用pytest运行测试用例
- test client 基于requests，使用方法类似

### 自动生成接口文档
- FastAPI支持自动生成Swagger UI & ReDoc两种风格的接口文档
- Swagger 风格的文档作为路由注册在[/doc](http://localhost:8000/docs)
- ReDoc 风格的文档作为路由注册在[/redoc](http://localhost:8000/redoc)

### 思考
- 如何实现类似flask_restful.Api类似的路由