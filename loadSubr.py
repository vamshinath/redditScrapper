from pymongo import  MongoClient
from pymongo.errors import DuplicateKeyError



client = MongoClient("localhost")
db = client["reddit"]
colls = db.list_collection_names()

colls.remove("subreddits")
allrd = colls
colls = list(filter(lambda x: "_user" in x,colls))


visitedSubr = list(map(lambda x:x["_id"],db["visited_sub_user"].find({})))

tmrds=[]
for ct in colls:
    tmrds.extend(list(db[ct].find({"viewed":False})))


recs=sorted(tmrds,key=lambda x: x["votes"],reverse=True)

for rd in recs:
    subr=rd["subreddit"]
    if subr not in visitedSubr and subr not in allrd:
        print(rd)
        collectionName = rd["collectionname"]
        db[collectionName].update_one({"_id":rd["_id"]},{"$set":{"viewed":True}})
        input("Enter for next:")
        db["visited_sub_user"].insert_one({"_id":subr})
        visitedSubr.append(subr)