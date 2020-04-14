## 1.基础使用
### 1.1创建app
```python
from celery import Celery
app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/1")

```
- tasks是当前的包名
- broker中间人可以有多种选择redis、RabbitMQ等。
- backend指定了结果存储的位置

### 1.2启动celery
```bash
celery -A tasks worker --loglevel=info
```
- tasks是人物所在的包名
- worker 参数指作为消费者进行执行
- `--loglevel`指定日志等级
- 更多命令`celery help` 

### 1.3调用task
```python
from tasks import add
res = add.delay(4, 4)
ready = res.ready()
result = res.get(timeout=1, propagate=False)
err = res.traceback()
```
- delay 函数调用执行任务， 返回的是AsyncResult对象
- ready检查任务是否执行完成
- get获取执行的结果(仅当配置了backend，任务未执行完毕时阻塞， 指定了timeout时会在超时时抛出错误), propagate参数指定在执行报错时是否重新抛出错误
- 若配置了资源进行结果存储，须调用get 或 forget进行资源释放

### 1.4配置选项
`app.config_from_object('config_file_name')`
- celery支持从对象(python模块或类)导入配置
```python
# config_file_name.py
broker_url = 'pyamqp://'
result_backend = 'rpc://'
task_serializer = 'json'  # 任务序列化的方式
result_serializer = 'json'  # 结果序列化的方式
accept_content = ['json']
timezone = 'Europe/Oslo'
enable_utc = True
task_routes = {  # 设置任务执行错误时的专用队列
    'tasks.add': 'low-priority',
}
task_annotations = {  # 针对任务进行限速，以下为每分钟内允许执行的10个任务的配置
    'tasks.add': {'rate_limit': '10/m'}
}
```

## 2.0 celery共享数据库会话
```python
from celery import Task


class DatabaseTask(Task):
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = Database.connect()
        return self._db
        
        
@app.task(base=DatabaseTask)
def process_rows():
    for row in process_rows.db.table.all():
        process_row(row)
```
- celery 支持基于类的任务，可以继承celery.Task类实现自定义的任务类
- 自定义的任务基类可以用单例模式初始化一个数据库会话，所有base未此基类的任务，都共享该连接

## 3.路由任务（路由、交换机和队列）配置
```python
from kombu import Exchange, Queue
app.conf.task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),  
    Queue('videos',  Exchange('media'),   routing_key='media.video'),
    Queue('images',  Exchange('media'),   routing_key='media.image'),
)
app.conf.task_routes = {
                        'project.tasks.*': {'queue': 'default'},  # 项目目录tasks相关任务发送至default队列
                        'project.videos.*': {'queue': 'videos'},  # 项目目录videos相关任务发送至videos队列
                        'project.images.*': {'queue': 'images'},  # 项目目录images相关所有任务发送至images队列
                        }

```
```bash
celery -A proj worker -Q default --hostname=x@%h  # 运行默认队列的职程
celery -A proj worker -Q videos --hostname=y@%h   # 运行videos队列的职程
celery -A proj worker -Q images --hostname=y@%h   # 运行images队列的职程
```
- [AMQP相关概念](https://www.cnblogs.com/qtiger/p/10071463.html)
- ![AMQP架构](https://img2018.cnblogs.com/blog/983950/201812/983950-20181205162817321-1993697263.png)
- 合理的配置不同的交换机和队列，可以使指定机器只执行指定类型的任务比如IO密集或计算密集等
