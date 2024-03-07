 #!/usr/bin/python3


#################################################################################################################################################
#                                                    CLASSES CONTAINING ALL THE APP FUNCTIONS                                                                                                    #
#################################################################################################################################################


import datetime
from app import mongo, Mqtt


class DB:

    def __init__(self,Config):

        
        from math import floor
        from os import getcwd
        from os.path import join
        from json import loads, dumps, dump
        from datetime import timedelta, datetime, timezone 
        from pymongo import MongoClient , errors, ReturnDocument
        from urllib import parse
        from urllib.request import  urlopen 
        from bson.objectid import ObjectId
        
       
      
        self.Config                         = Config
        self.getcwd                         = getcwd
        self.join                           = join 
        self.floor                      	= floor 
        self.loads                      	= loads
        self.dumps                      	= dumps
        self.dump                       	= dump  
        self.datetime                       = datetime
        self.ObjectId                       = ObjectId 
        self.server			                = Config.DB_SERVER
        self.port			                = Config.DB_PORT
        self.username                   	= parse.quote_plus(Config.DB_USERNAME)
        self.password                   	= parse.quote_plus(Config.DB_PASSWORD)
        self.remoteMongo                	= MongoClient
        self.ReturnDocument                 = ReturnDocument
        self.PyMongoError               	= errors.PyMongoError
        self.BulkWriteError             	= errors.BulkWriteError  
        self.tls                            = False # MUST SET TO TRUE IN PRODUCTION


    def __del__(self):
            # Delete class instance to free resources
            pass
 


    ####################
    # LAB 4 FUNCTIONS  #
    ####################
    
    # 1. CREATE FUNCTION TO INSERT DATA IN TO THE RADAR COLLECTION

    

def update_passcode(passcode):
    # Assuming your MongoDB collection is named 'code'
    code_collection = mongo.db.code

    # Check if a document already exists in the collection
    existing_document = code_collection.find_one({"type": "passcode"})

    if existing_document:
        # Update the existing document
        result = code_collection.update_one({"type": "passcode"}, {"$set": {"code": passcode}})
    else:
        # Insert a new document
        result = code_collection.insert_one({"type": "passcode", "code": passcode})

    # Check if the update/insert was successful
    return result.acknowledged


    
    # 2. CREATE FUNCTION TO RETRIEVE ALL DOCUMENTS FROM RADAR COLLECT BETWEEN SPECIFIED DATE RANGE. MUST RETURN A LIST OF DOCUMENTS

def check_passcode(passcode_to_check):
    # Assuming your MongoDB collection is named 'code'
    code_collection = mongo.db.code

    # Check if a document exists in the collection
    existing_document = code_collection.find_one({"type": "passcode", "code": passcode_to_check})

    # Return True if a matching document is found, else return False
    return existing_document is not None

    # 3. CREATE A FUNCTION TO COMPUTE THE ARITHMETIC AVERAGE ON THE 'reserve' FEILED/VARIABLE, USING ALL DOCUMENTS FOUND BETWEEN SPECIFIED START AND END TIMESTAMPS. RETURNS A LIST WITH A SINGLE OBJECT INSIDE
    
def update_and_publish_data(data):
    # Assuming your MongoDB collection is named 'code'
    code_collection = mongo.db.code

    # Assuming your MongoDB collection for the 'radar' data is named 'radar'
    radar_collection = mongo.db.radar

    # Extract passcode and timestamp from the received data
    passcode = data.get('code')
    timestamp = datetime.utcnow()

    try:
        # Use count_documents to check if a document with the received passcode exists
        count = code_collection.count_documents({"code": passcode})

        if count > 0:
            # Use find_one_and_update to update the 'code' field with upsert=True
            result = code_collection.find_one_and_update(
                {},
                {"$set": {"code": passcode, "timestamp": timestamp}},
                projection={'_id': False},
                upsert=True
            )

            # Publish the modified data to a topic subscribed by the frontend
            Mqtt.publish("frontend_topic", result)

            # Insert the modified object into the 'radar' collection
            radar_collection.insert_one(result)

            return True

        else:
            raise ValueError("Document with the provided passcode not found.")

    except Exception as e:
        raise ValueError(f"Failed to update and publish data. Error: {str(e)}")
    
    # 4. CREATE A FUNCTION THAT INSERT/UPDATE A SINGLE DOCUMENT IN THE 'code' COLLECTION WITH THE PROVIDED PASSCODE
   
def get_data_between_timestamps(start, end):
    try:
        # Convert start and end strings to datetime objects
        start_datetime = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
        end_datetime = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ")

        # Assuming your MongoDB collection is named 'radar'
        radar_collection = mongo.db.radar

        # Use find to retrieve data between the specified timestamps
        data = list(radar_collection.find({
            "timestamp": {"$gte": start_datetime, "$lte": end_datetime}
        }, projection={'_id': False}))

        return data

    except Exception as e:
        raise ValueError(f"Failed to retrieve data. Error: {str(e)}")
    
    # 5. CREATE A FUNCTION THAT RETURNS A COUNT, OF THE NUMBER OF DOCUMENTS FOUND IN THE 'code' COLLECTION WHERE THE 'code' FEILD EQUALS TO THE PROVIDED PASSCODE.
    #    REMEMBER, THE SCHEMA FOR THE SINGLE DOCUMENT IN THE 'code' COLLECTION IS {"type":"passcode","code":"0070"}

def calculate_average_between_timestamps(start, end):
    try:
        # Convert start and end strings to datetime objects
        start_datetime = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
        end_datetime = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ")

        # Assuming your MongoDB collection is named 'radar'
        radar_collection = mongo.db.radar

        # Use aggregate to calculate the average of 'reserve' field
        result = list(radar_collection.aggregate([
            {"$match": {"timestamp": {"$gte": start_datetime, "$lte": end_datetime}}},
            {"$group": {"_id": None, "average": {"$avg": "$reserve"}}}
        ]))

        # Check if any documents were found
        if result:
            return result[0]['average']

        return None

    except Exception as e:
        raise ValueError(f"Failed to calculate average. Error: {str(e)}")

   



def main():
    from config import Config
    from time import time, ctime, sleep
    from math import floor
    from datetime import datetime, timedelta
    one = DB(Config)
 
 
    start = time() 
    end = time()
    print(f"completed in: {end - start} seconds")
    
if __name__ == '__main__':
    main()


    
