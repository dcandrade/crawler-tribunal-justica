from pymongo import MongoClient
import config


class ProcessDAO():
    __instance = None

    def __init__(self):
        if ProcessDAO.__instance is None:
            self.__client = MongoClient("mongodb://mongodb:27017")  # TODO: change for docker instance
            self.__db = self.__client[config.DB_NAME]
        else:
            raise EnvironmentError("ProcessDAO is a singleton class. Use get_instance instead.")

    @staticmethod
    def get_instance():
        if ProcessDAO.__instance is None:
            __instance = ProcessDAO()

        return __instance

    def insert_process(self, court, process):
        self.__db[court].insert_one(process)

    def fetch_process(self, court, process_number):
        return self.__db[court].find_one({"_id": process_number})

    def close(self):
        self.__client.close()
