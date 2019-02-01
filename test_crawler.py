import unittest
from main import Crawler
from parameterized import parameterized


class TestPageLoad(unittest.TestCase):
    def setUp(self):
        self.crawlerTJSP = Crawler("TJSP")
        self.crawlerTJMS = Crawler("TJMS")

    def tearDown(self):
        self.crawlerTJSP.quit()
        self.crawlerTJMS.quit()

    def get_crawler(self, court):
        crawler = self.crawlerTJMS

        if(court == "TJSP"):
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
        ["TJSP", "1002298-86.2015.8.26.0271", 0],
        ["TJSP", "1002298-86.2025.8.26.0271", 1],
        ["TJSP", "0946027-47.1999.8.26.0100", 0],
        ["TJMS", "0821901-51.2018.8.12.0001", 0],
        ["TJMS", "0821901-51.2038.8.12.0001", 1],
    ])
    def test_enter_process_page(self, court, process_number, num_errors):
        crawler = self.get_crawler(court)


        n, f = crawler.get_descriptors(process_number)
        errors = crawler.enter_process_page(n, f)

        self.assertEqual(len(errors), num_errors)

    @parameterized.expand([
        ["tests/0000261-70.2010.8.12.0109 - TJMS.json"],
        ["tests/0025571-57.2011.8.26.0011 - TJSP.json"],
        ["tests/0039263-02.2018.8.12.0001 - TJMS.json"],
        ["tests/0821901-51.2018.8.12.0001 - TJMS.json"],
        ["tests/0946027-47.1999.8.26.0100 - TJSP.json"],
        ["tests/1002298-86.2015.8.26.0271 - TJSP.json"],
    ])
    def test_get_data(self, data_file):
        process_number, court = data_file.strip('.json').split(" - ")
        crawler = self.get_crawler(court)

        data = crawler.run(process_number)

        import json
        with open(data_file) as _data:
            reference_data = json.loads(_data.read())
        

        self.assertEqual(sorted(reference_data.items()), sorted(data.items()))



if __name__ == "__main__":
     unittest.main(warnings="ignore")



