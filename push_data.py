import os 
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGODB_URL = os.getenv("MONGO_DB_URL")
print(MONGODB_URL)

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def csv_to_json_converter(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records=records
            print("Attempting to connect to MongoDB...")
            self.mongo_client=pymongo.MongoClient(MONGODB_URL,tlsCAFile=ca)
            # test the connection
            self.mongo_client.admin.command('ping')
            print("MongoDB connection successful.")
            
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

if __name__ == '__main__':
    FILE_PATH="Network_Data\phisingData.csv"
    DATABASE="irfankarim"
    COLLECTION="NetworkData"
    networkobj=NetworkDataExtract()
    records=networkobj.csv_to_json_converter(file_path=FILE_PATH)
    print(f"Total {len(records)} records fetched from {FILE_PATH} file")
    no_of_records=networkobj.insert_data_mongodb(records,DATABASE,COLLECTION)
    print(f"Total {no_of_records} records inserted into {COLLECTION} collection of {DATABASE} database")
    print("Data inserted successfully")