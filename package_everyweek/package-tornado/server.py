# coding=utf-8
# builtins
# third party package
# self built
from tornado import ioloop, web


class MainHandler(web.RequestHandler):
    def get(self):
        self.write("hello world \n")
        self.write("hello world 2")

    def post(self):
        self.write("nice to meet u")


def get_app():
    return web.Application([
        ("/", MainHandler),
    ])

if __name__ == "__main__":
    app =get_app()
    app.listen(8080)
    ioloop.IOLoop.current().start()