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


class FeedbackHandler(tornado.web.RequestHandler):
    def post(self):
        arguments = tornado.escape.json_decode(self.request.body)
        data = arguments["data"]
        result = ""

        is_valid = (len(data) == 65)  # target(1) + data(64)
        if is_valid:
            try:
                [float(d) for d in data]
            except Exception as ex:
                is_valid = False

            if not (0 <= data[0] < 10):
                is_valid = False

        if is_valid:
            MachineLoader.feedback(machines.number_recognizer, data)
        else:
            result = "feedback format is wrong."

        resp = {"result": result}
        self.write(resp)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/predict", PredictionHandler),
            (r"/feedback", FeedbackHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )

        super(Application, self).__init__(handlers, **settings)


def main():
    # tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    port = int(os.environ.get("PORT", options.port))
    print("server is running on port {0}".format(port))
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(ex)
