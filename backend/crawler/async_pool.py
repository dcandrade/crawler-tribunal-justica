from concurrent.futures import ThreadPoolExecutor
from itertools import cycle
from crawler.workers import CrawlerWorker


class CrawlerPool:

    def __init__(self, court, size=1):
        """
        Manages multiple crawlers in order to perform multiple crawling requests simultaneously

        :param court: Court abbreviation (e.g. TJSP, TJMS)
        :param size: Number of crawlers contained in the pool
        """
        self.__crawlers_executors = []

        for _ in range(size):
            crawler = CrawlerWorker(court)
            executor = ThreadPoolExecutor(max_workers=1)
            self.__crawlers_executors.append((crawler, executor))

        self.__pool = cycle(self.__crawlers_executors)

    def add_task(self, process_number):
        """
        Adds a crawling task to the crawler pool

        :param process_number: Number of the process to be crawled (e.g. 0025571-57.2011.8.26.0011)
        :return: A future indicating when the crawling task is done
        """
        crawler, executor = next(self.__pool)
        result_future = executor.submit(crawler.run, process_number=process_number)
        executor.submit(crawler.reboot)

        return result_future

    def quit(self):
        """
        Free the allocated resources
        """
        for crawler, executor in self.__crawlers_executors:
            crawler.quit()
            executor.shutdown()
