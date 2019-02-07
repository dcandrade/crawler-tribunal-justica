from concurrent.futures import ThreadPoolExecutor
from itertools import cycle

from crawler.workers import CrawlerWorker


class CrawlerPool():

    def __init__(self, court, size=1):       
        self.crawlers_executors = []
        print("new crawler pool")

        for _ in range(size):
            crawler = CrawlerWorker(court)
            executor = ThreadPoolExecutor(max_workers=1)
            self.crawlers_executors.append((crawler, executor))

        self.pool = cycle(self.crawlers_executors)

    def add_task(self, process_number):
        crawler, executor = next(self.pool)
        print("sending")
        result_future = executor.submit(crawler.run, process_number=process_number)
        executor.submit(crawler.reboot)
        print("done")

        return result_future

    def quit(self):
        for crawler, executor in self.crawlers_executors:
            crawler.quit()
            executor.shutdown()
