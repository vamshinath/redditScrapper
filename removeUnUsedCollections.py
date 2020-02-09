from pymongo import MongoClient

cli = MongoClient("localhost")
db = cli["reddit"]

collection = db.list_collection_names()
safe_user = db["safer_user"]


already = list(map(lambda x:x["_id"],safe_user.find({})))

for nm in collection:
    if "user" in nm or nm in already:
        continue
    print("https://www.reddit.com/r/{}/".format(nm))
    ch=input("remove r/*:")
    if ch == "r":
        db.drop_collection(nm)
        print(nm,"removed")
    else:
        safe_user.insert_one({"_id":nm})
