import pytest
from main import Crawler

def test_descriptors():
    process_descriptors = {
        "1002298-86.2015.8.26.0271" : ("1002298-86.2015", "0271")
    }

    crawler = Crawler()
    for process_number, descriptor in process_descriptors.items():
        assert descriptor ==  crawler.get_descriptors(process_number)


