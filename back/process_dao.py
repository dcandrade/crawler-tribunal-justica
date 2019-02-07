from pymongo import MongoClient

class ProcessDAO():
    def __init__(self):
        self.client = MongoClient() #TODO: change for docker instance
        self.db = self.client['crawler-processes'] #TODO: static db name
        #TODO: index by process number

    def insert_process(self, court, process):
        self.db[court].insert_one(process)

    def fetch_process(self, court, process_number):
       return self.db[court].find_one({"_id":process_number})

#x = ProcessDAO()

#print(x.fetch_process("TJSP", "0946027-47.1999.8.26.0100"))