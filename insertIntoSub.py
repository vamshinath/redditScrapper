from pymongo import  MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient("localhost")
db = client["reddit2"]

while True:
    url = input("Enter Url:")
    try:
        db["subreddits"].insert_one({"_id":url,"active":True})
        print(url,"inserted")
    except DuplicateKeyError as e:
        e=0#db["subreddits"].update_one({"_id":url},{"$set":{"active":True}})
