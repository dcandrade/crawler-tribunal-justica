import unittest
from parameterized import parameterized

import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import config
config.TEST = True
from crawler.workers import _Crawler, CrawlerWorker
from utils.exceptions import InvalidProcessNumberException, PasswordProtectedProcessException
from db.process_dao import ProcessDAO

class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.crawlerTJSP = _Crawler("TJSP")
        self.crawlerTJMS = _Crawler("TJMS")

    def tearDown(self):
        self.crawlerTJSP.quit()
        self.crawlerTJMS.quit()

    def get_crawler(self, court):
        crawler = self.crawlerTJMS
        if (court == "TJSP"):
            crawler = self.crawlerTJSP
        return crawler

    @parameterized.expand([
        ["TJSP", "1002298-86.2015.8.26.0271", ("1002298-86.2015", "0271")],
        ["TJSP", "0946027-47.1999.8.26.0100", ("0946027-47.1999", "0100")],
        ["TJMS", "0821901-51.2018.8.12.0001", ("0821901-51.2018", "0001")],
    ])
    def test_descriptors(self, court, process_number, descriptor):
        crawler = self.get_crawler(court)
        self.assertEqual(descriptor, crawler.get_descriptors(process_number))

    @parameterized.expand([
        ["TJSP", "1002298-86.2015.8.26.0271", None],
        ["TJSP", "0025571-57.2011.8.26.0011", None],
        ["TJSP", "0946027-47.1999.8.26.0100", None],
        ["TJMS", "0821901-51.2018.8.12.0001", None],
        ["TJMS", "0000261-70.2010.8.12.0109", None],
        ["TJMS", "0039263-02.2018.8.12.0001", None],
        ["TJMS", "0831704-34.2013.8.12.0001", None],
        ["TJSP", "0000000-00.0000.8.26.0000", PasswordProtectedProcessException],
        ["TJMS", "1111111-11.1111.8.12.1111", InvalidProcessNumberException],
    ])
    def test_enter_process_page(self, court, process_number, exception=None):
        crawler = self.get_crawler(court)

        n, f = crawler.get_descriptors(process_number)

        if exception is None:
            result = crawler.enter_process_page(n, f)
            self.assertEquals(True, result)
        else:
            raised = False
            try:
                crawler.enter_process_page(n, f)
            except exception:
                raised = True

            self.assertTrue(raised)

    @parameterized.expand([
        ["tests/data/0000261-70.2010.8.12.0109 - TJMS.json"],
        ["tests/data/0025571-57.2011.8.26.0011 - TJSP.json"],
        ["tests/data/0039263-02.2018.8.12.0001 - TJMS.json"],
        ["tests/data/0821901-51.2018.8.12.0001 - TJMS.json"],
        ["tests/data/0946027-47.1999.8.26.0100 - TJSP.json"],
        ["tests/data/1002298-86.2015.8.26.0271 - TJSP.json"],
        ["tests/data/0831704-34.2013.8.12.0001 - TJMS.json"],
    ])
    def test_get_data(self, data_file, dump_test_data=True):
        process_number, court = data_file.strip('.json').split(" - ")
        process_number = process_number.split("/")[2]  # remove folder name

        crawler = self.get_crawler(court)

        n, f = crawler.get_descriptors(process_number)
        crawler.enter_process_page(n, f)

        data = crawler.extract_process_data()
        transactions = crawler.extract_transactions()
        parties = crawler.extract_parties()

        all_data = {**data, **parties, **transactions}

        import json
        with open(data_file) as _data:
            reference_data = json.loads(_data.read())

        if dump_test_data:
            with open(data_file.strip(".json") + "_test.json", 'w') as fp:
                json.dump(all_data, fp, sort_keys=True, indent=2, ensure_ascii=False)

        self.assertEqual(sorted(reference_data.items()), sorted(all_data.items()))

class TestCrawlerWorker(unittest.TestCase):
        config.DB_NAME = "worker-test"
        ProcessDAO.__instance = None # Resetting singleton
        dao = ProcessDAO.get_instance()
        db_client = dao._ProcessDAO__client 

        def setUp(self):
            TestCrawlerWorker.db_client.drop_database(config.DB_NAME)
            self.crawlerTJSP = CrawlerWorker("TJSP")
            self.crawlerTJMS = CrawlerWorker("TJMS")

        def tearDown(self):
            self.crawlerTJSP.quit()
            self.crawlerTJMS.quit()

        def get_crawler(self, court):
            crawler = self.crawlerTJMS

            if (court == "TJSP"):
                crawler = self.crawlerTJSP

            crawler.reboot()

            return crawler

        @parameterized.expand([
            ["tests/data/0000261-70.2010.8.12.0109 - TJMS.json"],
            ["tests/data/0025571-57.2011.8.26.0011 - TJSP.json"],
            ["tests/data/0039263-02.2018.8.12.0001 - TJMS.json"],
            ["tests/data/0821901-51.2018.8.12.0001 - TJMS.json"],
            ["tests/data/0946027-47.1999.8.26.0100 - TJSP.json"],
            ["tests/data/1002298-86.2015.8.26.0271 - TJSP.json"],
            ["tests/data/0831704-34.2013.8.12.0001 - TJMS.json"],
        ])
        def test_acquisition(self, data_file):
            process_number, court = data_file.strip('.json').split(" - ")
            process_number = process_number.split("/")[2]  # remove folder name

            db_data = TestCrawlerWorker.dao.fetch_process(court, process_number)

            self.assertIsNone(db_data)

            crawler = self.get_crawler(court)
            data = crawler.run(process_number)
            db_data = TestCrawlerWorker.dao.fetch_process(court, process_number)

            self.assertEqual(sorted(data.items()), sorted(db_data.items()))

if __name__ == "__main__":
    unittest.main(warnings="ignore")
