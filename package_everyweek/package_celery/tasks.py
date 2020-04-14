# coding=utf-8
# builtins
# third party package
from celery import Celery
# self built


app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/1")


@app.task
def add(a, b):
    return a + b
