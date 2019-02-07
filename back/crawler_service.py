from multiprocessing import Queue
from multiprocessing import Process
from crawler import Crawler
from config import COURTS

class CrawlerPool():
    # TODO: specify TJSP and TJMS specific crawlers for speed
    def __init__(self, court, size=1):
        self.court = court
        self.task_queue = Queue()
        self.crawlers = []
        self.threads = []
        self.results = {}

        for _ in range(size):
            crawler = Crawler(court)
            self.crawlers.append(crawler)
            crawler_thread = Process(target=crawler.run_queue, args=[self.task_queue])
            crawler_thread.start()
            self.threads.append(crawler_thread)
        print("done initialization")

        # task queue item = (pid, callback)
    def add_task(self, process_number, callback):
        self.task_queue.put((process_number, callback))

    def quit(self):
        for i in range(len(self.crawlers)):
            self.crawlers[i].quit()
        
        for p in self.threads:
            p.terminate()


#c = CrawlerPool("TJSP")
#process_number = "0633677-76.1994.8.26.0100"
#c.add_task(process_number, print)

