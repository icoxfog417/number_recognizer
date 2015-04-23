import os
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.escape
from tornado.options import define, options
from machines.machine_loader import MachineLoader
import machines.number_recognizer
from machines.number_recognizer.validator import Validator


# Define command line arguments
define("port", default=3000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", title="title")


class BaseHandler(tornado.web.RequestHandler):
    MACHINE_SESSION_KEY = "number_recognizer"


class PredictionHandler(BaseHandler):

    def post(self):
        resp = {"result": str(-1)}
        data = self.get_arguments("data[]")
        # print(data)

        validated = Validator.validate_data(data)
        machine = MachineLoader.load(machines.number_recognizer)
        if len(validated) > 0:
            predicted = machine.predict(validated)
            resp["result"] = str(predicted[0])

        self.write(resp)


class FeedbackHandler(BaseHandler):

    def post(self):
        data = self.get_arguments("data[]")
        result = ""

        feedback = Validator.validate_feedback(data)
        if len(feedback) > 0:
            MachineLoader.feedback(machines.number_recognizer, feedback)
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
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            xsrf_cookies=True,
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
