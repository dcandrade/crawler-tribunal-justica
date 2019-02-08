from concurrent.futures import ThreadPoolExecutor
from itertools import cycle
from crawler.workers import CrawlerWorker

class CrawlerPool():

    def __init__(self, court, size=1):       
        self.__crawlers_executors = []

        for _ in range(size):
            crawler = CrawlerWorker(court)
            executor = ThreadPoolExecutor(max_workers=1)
            self.__crawlers_executors.append((crawler, executor))

        self.__pool = cycle(self.__crawlers_executors)

    def add_task(self, process_number):
        crawler, executor = next(self.__pool)
        result_future = executor.submit(crawler.run, process_number=process_number)
        executor.submit(crawler.reboot)

        return result_future

    def quit(self):
        for crawler, executor in self.__crawlers_executors:
            crawler.quit()
            executor.shutdown()
