from pymongo import MongoClient
import config


class ProcessDAO:
    __instance = None

    def __init__(self):
        """
        Wrapper for fetch and insert process data from db
        """
        if ProcessDAO.__instance is None:
            if config.TEST:
                self.__client = MongoClient()
            else:
                self.__client = MongoClient("mongodb://mongodb:27017")
                
            self.__db = self.__client[config.DB_NAME]
        else:
            raise EnvironmentError("ProcessDAO is a singleton class. Use get_instance instead.")

    @staticmethod
    def get_instance():
        """
        Get current ProcessDAO instance
        :return: ProcessDAO instance
        """
        if ProcessDAO.__instance is None:
            ProcessDAO.__instance = ProcessDAO()

        return ProcessDAO.__instance

    def insert_process(self, court, process):
        """
        Insert a process on db
        :param court: Court of the process to be inserted
        :param process: Process data
        """
        self.__db[court].insert_one(process)

    def fetch_process(self, court, process_number):
        """
        Fetch a process from db
        :param court: Court of the process to be inserted
        :param process_number: Number of the process to be fetched
        :return: A dict contaning the process data if the process is present or None otherwise
        """
        return self.__db[court].find_one({"_id": process_number})

    def close(self):
        """
        Close connection with db
        """
        self.__client.close()
