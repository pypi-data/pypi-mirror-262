import os
from a2ginputstream.cloud_inputstream import CloudInputstream
from a2ginputstream.local_inputstream import LocalInputstream

class A2GClient:
    
    def __init__(self, token:str, cache_options:dict = None):
        """
        Constructor for the A2GClient class. the cache is only to local development, in the cloud the cache is not used.
        :param token: The token to be used for authentication and valindattion of resources used by the client
        :param cache_options: A dictionary containing the options for the cache. {"duration_data": int, "duration_inputstream": int},  the values are minutes and default is 1440 minutes (24 hours) in both cases. 
        """
        raise NotImplementedError("This class is not meant to be instantiated")
    
    def get_inputstream_schema(self, ikey:str, cache = True) -> dict:
        """
        Get the schema of the inputstream
        """   
        pass

    def find(self, ikey, query:dict, cache = True):
        """
        Find the data in the inputstream.
        :param ikey: The inputstream ikey
        :param query: Dictiony with pymongo syntax
        :param cache: If true, try to recover the data from the cache, if false, the data is downloaded from the A2G
        """
        pass    

    def find_one(self, ikey, query:dict, cache = True):
        """
        Find one data in the inputstream. Only retrieves the first element that matches the query
        :param ikey: The inputstream ikey
        :param query: Dictiony with pymongo syntax
        :param cache: If true, try to recover the data from the cache, if false, the data is downloaded from the A2G
        """
        pass

    def get_data_aggregate(self, ikey:str, query: list[dict], cache = True): 
        """
        Get the data from the inputstream using aggregation, The write operations are not allowed in this method
        :param ikey: The inputstream ikey
        :param query: List of dictionaries with pymongo syntax
        :param cache: If true, try to recover the data from the cache, if false, the data is downloaded from the A2G
        """
        pass

    def insert_data(self, ikey:str, data:list[dict], cache = True):
        """
        Insert data into the inputstream
        :param ikey: The inputstream ikey
        :param data: List of dictionaries with the data to be inserted
        :param cache: If true, it validate the data with the schema in the cache.
        """
        pass


__mode = os.environ.get("EXEC_LOCATION", "LOCAL")

if __mode == "LOCAL":
    A2GClient = LocalInputstream
elif __mode == "CLOUD":
    A2GClient = CloudInputstream
else:
    raise ValueError("EXEC_LOCATION must be either LOCAL or CLOUD")