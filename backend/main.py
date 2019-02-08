import tornado.ioloop
import tornado.web
from tornado import gen
import json

import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from crawler.async_pool import CrawlerPool
import config

# Start one pool for each court
POOLS = {court: CrawlerPool(court, config.POOL_SIZE) for court in config.COURTS}


class MainHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self):
        process_number = self.get_argument("process_number")
        court = self.get_argument("court")
        response = yield POOLS[court].add_task(process_number)
        self.write(response)


class StopHandler(tornado.web.RequestHandler):
    def get(self):
        for _, pool in POOLS.items():
            pool.quit()
        self.write("done")


class CourtHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps({"courts": config.COURTS}))


def make_app():
    return tornado.web.Application([
        (r"/get_process", MainHandler),
        (r"/stop", StopHandler),
        (r"/courts", CourtHandler)
    ], debug=False)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Backend server online")
    tornado.ioloop.IOLoop.current().start()
