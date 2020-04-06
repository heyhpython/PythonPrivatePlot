
## 1.协程的几种类型
### 1.1 基于生成器的协程
```python
import asyncio

@asyncio.coroutine
def func():
    yield 1
```
- 此方式已启用，将于`3.10`版本删除

### 1.2 基于`async`和`await`关键字的携程
```python
import asyncio

async  def func():
    await asyncio.sleep(1)
```
- `asyncio.iscoroutine(obj)`如果是协程对象返回`True`,不同于 `inspect.iscoroutine()` 因为它对基于生成器的协程返回`True`
- `asyncio.iscoroutinefunction(func)`让如果是协程函数返回`True`, 不同于 `inspect.iscoroutinefunction()` 因为它对以 `@coroutine` 装饰的基于生成器的协程函数返回 `True`。



## 2.携程的使用

```python
import asyncio

async def main():
    print("hello")
    await asyncio.sleep(1)
    print("world")

asyncio.run(main())
asyncio.create_task(main())
```
- 简单的调用一个携程函数并不会将其加入到执行日程，而是会返回一个协程对象
- `asyncio.create_task`函数用来`并发`的运行作为`asyncio`的多个协程

### 2.1 `asyncio.run(coro, *, debug=False)`运行协程
- 此函数运行传入的协程，负责管理 `asyncio` 事件循环
- 当有其他`asyncio`事件循环在同一线程中运行时，此函数不能被调用
- 此函数总是会创建一个新的事件循环并在结束时关闭，它应当被当作`asyncio`程序的主入口，只被调用一次

### 2.2 创建任务运行协程
```python
import asyncio  

async def coro():
    return 1

# python 3.7+
task1 = asyncio.create_task(coro())
# all version
task2 = asyncio.ensure_future(coro())
```
- 将 coro 协程 打包为一个 Task 排入日程准备执行。返回 Task 对象。
- 该任务会在`get_running_loop()`返回的事件循环中执行，如果当前线程没有再运行的事件循环，则会引发运行时错误

### 2.3 `asyncio.sleep`协程的休眠
```python
import asyncio
import datetime

async def display_date():
    loop = asyncio.get_running_loop()
    end_time = loop.time() + 5
    while 1:
        print(datetime.datetime.now())
        if (loop.time() + 1) >= end_time:
            break
        await asyncio.sleep(1)

asyncio.run(display_date())
```
- `asyncio.sleep`总会挂起当前任务，但会允许其他任务运行


### 2.4 `asyncio.gather`并发的运行任务
```python
import asyncio

async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")

async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )
```
- 传入可等待对象的序列，并发的运行
- 所有的可等待对象都成功完成，结果是一个所有返回值聚合的列表，顺序与传入的一致
- `return_exceptions`参数默认为False, 所引发的首个异常会立即传播给等待`gather`的任务，但是序列中的其他可等待对象不会被取消执行
- `return_exceptions`参数为`True`时，异常会和成功的结果一样，被聚合到结果的列表
- 如果`gather`被取消， 所有提交但尚未完成的可等待对象也会被取消
- 可等待对象中的任一可等待对象被取消，不会影响其他同时`gather`的任务

### 2.5 屏蔽取消操作`asyncio.shield(aw, *, loop=None)`
```
res = await shiled(coro())
# 相当于
res = await coro()
```
- `shiled`保护一个可等待对象，防止其被取消
- 如果aw时协程，会自动被加入日程
- 是否使用shield的区别在于，如果包含它`coro()`的协程被取消， `coro()`不会被取消
- 如果是`coro()`协程内部取消，则`shield`也会取消

### 2.6 超时`asyncio.wait_for(aw, timeout, *, loop=None)`
```python
import asyncio

async def eternity():
    # Sleep for one hour
    await asyncio.sleep(3600)
    print('yay!')

async def main():
    # Wait for at most 1 second
    try:
        await asyncio.wait_for(eternity(), timeout=1.0)
    except asyncio.TimeoutError:
        print('timeout!')

asyncio.run(main())
```
- 等待可等待对象完成，指定的`timeout`后超时
- 如果aw是协程，会自动作为任务加入到日程
- 若`timeout`为`None`则直到任务完成
- 若超时，则任务会取消，并引发超时错误
- 如要避免取消， 可以加上`shield`
- 函数将等待直到目标任务确实被取消
- 如果等待被取消，则任务也会被取消

### 2.7简单等待`asyncio.wait(aws, *, loop=None, timeout=None, return_when=ALL_COMPLETED)
```
done, pending = await asyncio.wait(aws)
```
- 并发的运行指定的可等待对象并阻塞线程直到满足`return_when`指定的条件
- 直接传入协程会将协程加入日程，但是会导致用户的困惑，因此已启用
- 返回两个`Task/Future`的集合
- 如果指定`timeout`则将被用于控制返回之前的等待最长秒数，但不会引发超时错误
- 与`wait_for`不同，`wait`超时不会取消可等待对象，只会决定函数在何时返回
- `return_when`指定此函数在何时返回

### 2.7 多线程的日程`asyncio.run_coroutine_threadsafe(coro, loop)`
- 向指定的事件循环中提交一个协程， 线程安全
- 返回一个`Future`对象，等待其他线程的结果
- 此函数应在另一个线程中调用，而不是事件循环运行的线程

### 内省
- `asyncio.current_task(loop=None)` 返回事件循环中当前运行的Task实例
- `asyncio.all_tasks(loop=None)`返回事件循环中所有未完成的任务对象集合


## 3.可等待对象
### 3.1定义
- 如果一个对象可以在 `await` 语句中使用，那么它就是可等待对象。
- 许多 asyncio API 都被设计为接受可等待对象。

### 3.2分类
#### 3.2.1 协程
- python协程属于可等待对象
- 协程指的是`协程函数`和`协程对象`
- `协程函数`时定义为`async def`的函数
- `协程对象` 调用协程函数返回的对象
- `asyncio`也支持基于生成器的协程

#### 3.2.2 `Task`对象
```python
import asyncio

async def nested():
    return 42

async def main():

    task = asyncio.create_task(nested())

    # "task" can now be used to cancel "nested()", or
    # can simply be awaited to wait until it is complete:
    await task

asyncio.run(main())
```
- 任务被用来设置日程以便并发执行协程
- 当协程通过`asyncio.create_task`等函数打包为任务，该写程自动排入日程准备运行


#### 3.2.3 `Future`对象
- `Future`是底层及的可等待对象，表示异步操作的最终结果
- 当`Future`对象被等待，意味着协程将保持等待直到`Future`对象在其他地方的操作完毕

#4.事件循环
[文档](https://docs.python.org/zh-cn/3.7/library/asyncio-eventloop.html#asyncio.loop.run_in_executor)


### 4.1获取事件循环

- `asyncio.get_running_loop()`获取当前线程中的事件循环，没有则引发运行时错误，函数只能由协程或回调来调用
- `asyncio.get_event_loop()` 获取当前的事件循环，当前线程没有事件循环且是主线程并且尚未调用`set_event_loo()`，会自动创建新的事件循环并设置为当前事件循环
- `asyncio.set_event_loop(loop)`设置为当前线程的当前事件循环
- `asyncio.new_event_loop()` 创建新的事件循环 

### 4.2运行和停止循环
 `loop.run_until_complete(future)`
- 运行到`future(Future实例)`被完成
- 如果是协程对象， 责备隐式的调度为`Task`
- 返回`Future`的结果或抛出异常

`loop.run_forever()`
- 运行事件循环直到`stop()`被调用
- 若`stop()`在`run_forever()`之前调用，会运行已经加入到日程的回调然后退出
- 若`stop()`在`run_forever()`之时调用，会运行当前一批回调然后退出， 回调的产生的新的回调不会被运行，但是会在下一次`run_forever()`或`run_until_complete()`被调用

`loop.stop()`
- 停止事件循环

`loop.close()`
- 关闭事件循环

`loop.is_runing()`，`loop.is_cloese()`
- 查看循环是否在运行或关闭

`loop.shudown_asyncgens()`
- 调用`agen.aclose()`关闭所有当前打开的异步生成器
- 当使用`asyncio.run()`时， 无需调用此函数

### 4.3调度回调

`loop.call_soon(callback, *args, context=None)`
- 在下次事件循环的迭代中使用`args`参数调用`callback`
- 回调按注册顺序被调用一次
- 可选参数`context`允许`callback`运行在一个指定`contextvars.Context`对象中，若无则使用当前上下文
- 返回一个能用来取消回调的`asyncio.Handle`实例
- 此方法不是线程安全

`loop.call_soon_threadsafe(callback, *args, context=None)`
- `call_soon`的线程安全变体， 被用来安排来自其他线程的回调
- 大多数`asyncio`调度函数不支持关键字参数，可使用`functools.partial`

### 4.4调度延迟回调

`loop.call_later(delay, callback, *args, context=None)`
- 在指定的`delay`之后调用回调
- 返回一个`asyncio.TimerHandler`实例， 用于取消回调
- `3.7.1`版本前，`delay`不可超过一天

`loop.call_at(when, callback, *args, context=None)`
- 在给定的时间戳执行回调,·`when`时整型或者浮点型的时间戳
- `3.7.1`版本前，`when`与当前时间差不可超过一天
- 其他同`call_later`

`loop.time()`
- 根据事时间循环内部的单调时钟，返回当前时间的浮点值


## 5.使用`asyncio`开发

### 5.1 `Debug`