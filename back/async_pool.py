from multiprocessing import Queue
from multiprocessing import Process
from crawler import CrawlerWorker
from concurrent.futures import ThreadPoolExecutor
from itertools import cycle

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


#x = CrawlerPool("TJSP")
#f = x.add_task("0633677-76.1994.8.26.0100")

