from pymongo import  MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient("mongodb+srv://ubuntuVM:vamshi81@mymongo-yiker.azure.mongodb.net/reddit?retryWrites=true&w=majority")
db = client["reddit"]

while True:
    url = input("Enter Url:")
    try:
        db["subreddits"].insert_one({"_id":url})
        print(url,"inserted")
    except DuplicateKeyError as e:
        print("key Error")
