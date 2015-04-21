import os
import json
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.escape
from tornado.options import define, options
from machines.machine_loader import MachineLoader
import machines.number_recognizer


# Define command line arguments
define("port", default=3000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", title="title")


class PredictionHandler(tornado.web.RequestHandler):
    def post(self):
        arguments = tornado.escape.json_decode(self.request.body)
        data = arguments["data"]
        # print(data)
        machine = MachineLoader.load(machines.number_recognizer)
        predicted = machine.predict(data)
        resp = {"result": str(predicted[0])}
        self.write(resp)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/predict", PredictionHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )

        super(Application, self).__init__(handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    port = int(os.environ.get("PORT", options.port))
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
