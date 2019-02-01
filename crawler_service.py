from multiprocessing import Queue
from multiprocessing import Process
from crawler import Crawler
from config import COURTS

class CrawlerPool():
    # TODO: specify TJSP and TJMS specific crawlers for speed
    def __init__(self, size=1):
        self.task_queue = {}
        self.crawlers = {}
        self.threads = []

        for court in COURTS:
            self.task_queue[court] = Queue()
            self.crawlers = []

        for _ in range(size):
            for court in self.crawlers:
                crawler = Crawler(court)
                self.crawlers[court].append(crawler)
                crawler_thread = Process(target=crawler.run_queue, args=[self.task_queue[court]])
                crawler_thread.start()
                self.threads.append(crawler_thread)

        # task queue item = (pid, callback)
    def add_task(self, process_number, court, callback):
        self.task_queue[court].put((process_number, callback))

    def quit(self):
        for court in COURTS:
            for i in range(len(self.crawlers[court])):
                self.crawlers[court][i].quit()
        
        for p in threads:
            p.terminate()



c = CrawlerPool()
    
c.add_task("0633677-76.1994.8.26.0100", "TJSP", print)
from time import sleep
sleep(120)
c.quit()

