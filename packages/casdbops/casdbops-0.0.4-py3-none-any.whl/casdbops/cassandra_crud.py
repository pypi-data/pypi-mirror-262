import os
import pandas as pd
import json
from astrapy.ops import AstraDBOps
from astrapy.db import AstraDB,AstraDBCollection


class cassandra_operation:
    '''Firstly , User has to make account on Astra DB platform. Then User need to provide following credentials For establishing connection :- 
    1. Password of his/her  Astra DB account
    1. Token -> {Go to Dashboard , Generate Token (seelct Organisation Admin from dropdown)}
    3. Database Name
    After Creation of DataBase Copy API Endpoint from User dashboard And provide it for creating collection 
    Give Collection Name
    Give Dataset path'''
    def __init__(self,token):
        self.client=AstraDBOps(token)
        self.token = token
    
    def create_database(self,database_name="test",passwd=None):
        self.database_name=database_name
        if passwd!=None:
            try:
                database_definition = {
                    "name": self.database_name,
                    "tier": "serverless",
                    "cloudProvider": "GCP", # GCP, AZURE, or AWS
                    "keyspace": "default_keyspace",
                    "region": "us-east1",
                    "capacityUnits": 1,
                    "user": self.token.split(':')[1],
                    "password": passwd,
                    "dbType": "vector"}
                self.DB_response = self.client.create_database(database_definition=database_definition)   
                return self.DB_response 
            except Exception as e:
                print(e)   
        else:
             print("Password Not provided")
             return 

    def connect_to_database(self,api_endpoint=None):
        if api_endpoint!=None:
            try:
                self.db = AstraDB(
                        token=self.token,
                        api_endpoint=api_endpoint)
                return self.db
            except Exception as e:
                print(e)
        else:
             print("API_end point Not provided")
             return

    def create_collection(self,collection_name="Collection_test"):
        self.collection_name = collection_name
        try:
            # create new collection        
            self.collection_obj = AstraDBCollection(collection_name=self.collection_name, astra_db=self.db)

            # Delete all documents in the collection
            self.collection_obj.delete_many(filter={})
            return self.collection_obj
        except Exception as e:
            print(e)
        return
    
    def insert_into_collection(self,dataset_path=None):
        if dataset_path!=None:
            try:
                if dataset_path.endswith('.csv'):
                    df = pd.read.csv(dataset_path,encoding='utf-8')
                    
                elif dataset_path.endswith(".xlsx"):
                    df = pd.read_excel(dataset_path,encoding='utf-8')

                json_list = []

                # Iterate through each row of the DataFrame
                for index, row in df.iterrows():
                    # Create a dictionary for each row
                    row_dict = dict(zip(row.index, row.tolist()))
                    # Append the dictionary to the list
                    json_list.append(row_dict)

                responses = self.collection_obj.chunked_insert_many(
                            documents=json_list,
                            chunk_size=20,  # Chunk size set to 20 documents
                            concurrency=20)  # Concurrently insert 20 chunks at a time
                print("Successfully Inserted Documents into collection ")
                return
            except Exception as e:
                print(e)
        else:
            print("Invalid Dataset path ")
            return
        
    def Fetch_data_from_collection(self,):
        try:
            generator = self.collection_obj.paginated_find(
                        filter={},
                        options={})

            list_fetch = list()
            for doc in generator:
                list_fetch.append(doc)
            df_retrieved = pd.DataFrame(list_fetch).drop('_id',axis=1)
            return df_retrieved
        except Exception as e:
            print(e)
            return