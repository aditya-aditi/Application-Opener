import pymongo

def connect_to_db():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client['application_opener']
    collection = db['applications']
    print("Connection successful!")