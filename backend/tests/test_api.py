import unittest
import json
from parameterized import parameterized
import tornado.platform.asyncio as tasyncio
from tornado import testing, web
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import config
config.TEST = True
from main import CourtHandler, MainHandler
from crawler.workers import CrawlerWorker

os.environ["ASYNC_TEST_TIMEOUT"] = "500"


class TestGetProcess(testing.AsyncHTTPTestCase):
    def setUp(self):
        super().setUp()
        self.crawlerTJSP = CrawlerWorker("TJSP")
        self.crawlerTJMS = CrawlerWorker("TJMS")

    def tearDown(self):
        super().tearDown()
        self.crawlerTJSP.quit()
        self.crawlerTJMS.quit()

    def get_crawler(self, court):
        crawler = self.crawlerTJMS
        if (court == "TJSP"):
            crawler = self.crawlerTJSP
        return crawler

    def get_app(self):
        return web.Application([('/get', MainHandler)])

    def get_new_ioloop(self):
        return tasyncio.AsyncIOMainLoop()
    
    @parameterized.expand([
        ["TJSP", "1002298-86.2015.8.26.0271"],
        ["TJSP", "0025571-57.2011.8.26.0011"],
        ["TJSP", "0946027-47.1999.8.26.0100"],
        ["TJMS", "0821901-51.2018.8.12.0001"],
        ["TJMS", "0000261-70.2010.8.12.0109"],
        ["TJMS", "0039263-02.2018.8.12.0001"],
        ["TJMS", "0831704-34.2013.8.12.0001"],
        ["TJSP", "0000000-00.0000.8.26.0000"],
        ["TJMS", "1111111-11.1111.8.12.1111"],
    ])
    def test_get(self, court, process_number):
        response = self.fetch('/get_process?court={}&process_number={}'.format(court, process_number), method="GET").body
        response = json.loads(response)
        expected_response = self.get_crawler(court).run(process_number)
        self.assertEqual(sorted(expected_response.items()), sorted(response.items()))

    
if __name__ == "__main__":
    unittest.main(warnings="ignore")
