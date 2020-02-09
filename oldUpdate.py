from pymongo import MongoClient
import time

cl = MongoClient("localhost")
db = cl["reddit"]

collections = db.list_collection_names()



alldata=[]
for collectionString in collections:
    if "_user" in collectionString:
        rec=db[collectionString].delete_many({"viewed":True})
        print(str(rec))
    continue
    collection = db[collectionString]
    alldata=list(collection.find({}))
    for dct in alldata:
        collection.update_one({"_id":dct["_id"]},{"$set":{"numComments":0}})

