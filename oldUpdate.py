from pymongo import MongoClient


cl = MongoClient("localhost")
db = cl["reddit"]

collections = db.list_collection_names()

alldata=[]
for collectionString in collections:
    collection = db[collectionString]
    alldata=list(collection.find({}))
    for dct in alldata:
        collection.update_one({"_id":dct["_id"]},{"$set":{"numComments":0}})

