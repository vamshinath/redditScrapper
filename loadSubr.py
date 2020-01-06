from pymongo import  MongoClient
from pymongo.errors import DuplicateKeyError



client = MongoClient("localhost")
db = client["reddit"]
colls = db.list_collection_names()

colls.remove("subreddits")
colls.remove("loves_DND")
allrd = colls
colls = list(filter(lambda x: "_user" in x,colls))


visitedSubr = list(map(lambda x:x["_id"],db["visited_sub_user"].find({})))

tmrds=[]
for ct in colls:
    tmrds.extend(list(db[ct].find({"viewed":False})))


search = input("Enter key:")
if search:
    tmrds = list(filter(lambda x: search.lower() in x["title"].lower(),tmrds))
    print("search",len(tmrds))


if input("only 18(y/*):") == "y":
    tmp = []
    for twt in tmrds:
        try:
            if twt["over18"]:
                tmp.append(twt)
        except Exception as e:
            e=0
    if tmp:
       tmrds = tmp


if input("Enter sb for subreddit sort/votes(*):") == "sb":
    recs=sorted(tmrds,key=lambda x: x["subreddit"],reverse=True)
else:
    recs=sorted(tmrds,key=lambda x: x["votes"],reverse=True)

for rd in recs:
    subr=rd["subreddit"]
   
    if subr not in visitedSubr and subr not in allrd:
        print("https://www.reddit.com/r/{}/".format(subr))
        print(rd)
        collectionName = rd["collectionname"]
        db[collectionName].update_one({"_id":rd["_id"]},{"$set":{"viewed":True}})
        ch = input("Enter insert(i)/*:")
        db["visited_sub_user"].insert_one({"_id":subr})
        visitedSubr.append(subr)
        if ch == "i":
            try:
                url="https://www.reddit.com/r/{}/".format(subr)
                db["subreddits"].insert_one({"_id":url})
                print(url+" added")
            except Exception as e:
                print(e)
