import tornado.ioloop
import tornado.web
from tornado import gen
from async_pool import CrawlerPool
import config
import json

POOLS = {court:CrawlerPool(court, config.POOL_SIZE) for court in config.COURTS}

class MainHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self):
        process_number = self.get_argument("process_number")
        court = self.get_argument("court")
        print("-----------", process_number, "----", court)
        response = yield POOLS[court].add_task(process_number)
        self.write(response)

class StopHandler(tornado.web.RequestHandler):
        def get(self):
            for _, pool in POOLS.items():
                pool.quit()
            self.write("done")

class CourtHandler(tornado.web.RequestHandler):
        def get(self):
            self.write(json.dumps({"courts":config.COURTS}))
    

def make_app():
    return tornado.web.Application([
        #(r"/get", MainHandler, dict(court="TJSP"))
        (r"/get", MainHandler),
        (r"/stop", StopHandler),
        (r"/courts", CourtHandler)

    ], debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()