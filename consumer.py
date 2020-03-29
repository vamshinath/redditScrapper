from pymongo import  MongoClient
from pymongo.errors import DuplicateKeyError

import humanize,sys,time
from selenium import webdriver


client = MongoClient("localhost")
db = client["reddit2"]


colls = db.list_collection_names()

colls.remove("subreddits")

print(colls)

print("{'title': 'Beauty', 'subreddit': 'JacquelineFernandez', 'votes': 1, 'score': 1, 'timestamp': 1407207076.0, 'url': 'http://i.imgur.com/W7EpTBD.jpg', 'author': 'Emwat1024', 'flsz': 488402, 'group': '2014-08-05', 'numComments': 0, 'over18': False, '_id': '2cm29l', 'viewed': False, 'collectionname': 'JacquelineFernandez'}")


collection = input("Enter collection:")
searchKey = input("Enter searchKey")
sortKey = input("Enter sortKey:")

if sortKey == "":
    sortKey = "timestamp"

posts = []
if collection == "":
    for ct in colls:
        if searchKey == "":
            posts+= list(db[ct].find({"viewed":False}))
        else:
            posts+= list(db[ct].find({"viewed":False,"title":{"$regex":searchKey,"$options":"i"}}))
else:
    if searchKey == "":
        posts+= list(db[collection].find({"viewed":False}))
    else:
        posts+= list(db[collection].find({"viewed":False,"title":{"$regex":searchKey,"$options":"i"}}))

posts = sorted(posts,key=lambda x: x[sortKey],reverse=True)


if sortKey == "timestamp":
    final={}
    dts=[]
    for post in posts:
        datee = post["group"]
        if datee not in dts:
            dts.append(datee)


    for dt in dts:
        data = []
        for post in posts:
            datee = post["group"]
            if datee == dt:
                data.append(post)
                posts.remove(post)
        final[dt]=data

    final = sorted(final.items(),key=lambda x: int(x[0].replace("-","")),reverse=True)

    chrome = webdriver.Chrome("./chromedriver")
    chrome.get("http://www.e-try.com/black.htm")
    for ky,val in final:
        posts = sorted(val,key=lambda x:x["flsz"],reverse=True)
        for post in posts:
            subr = post["collectionname"]
            title = post["title"]
            votes = post["votes"]
            datee = post["group"]
            flsz = post["flsz"]
            print(post["author"])
            print(subr+"\n"+title+"\n"+str(votes)+"\n"+datee+"\n"+"\n"+post["url"])
            print(humanize.naturalsize(flsz))
            print(post["_id"])
            try:
                chrome.execute_script("window.open({},'_blank')".format("'"+post["url"]+"'"))
            except Exception as e:
                sys.exit(1)
            while len(chrome.window_handles) > 1:
                time.sleep(1.5)
            db[subr].update_one({"_id":post["_id"]},{"$set":{"viewed":True}})
        

else:
    chrome = webdriver.Chrome("./chromedriver")
    chrome.get("http://www.e-try.com/black.htm")
    for post in posts:
        subr = post["collectionname"]
        title = post["title"]
        votes = post["votes"]
        datee = post["group"]
        flsz = post["flsz"]
        print(post["author"])
        print(subr+"\n"+title+"\n"+str(votes)+"\n"+datee+"\n"+"\n"+post["url"])
        print(humanize.naturalsize(flsz))
        print(post["_id"])
        try:
            chrome.execute_script("window.open({},'_blank')".format("'"+post["url"]+"'"))
        except Exception as e:
            sys.exit(1)
        while len(chrome.window_handles) > 1:
            time.sleep(1.5)

        db[subr].update_one({"_id":post["_id"]},{"$set":{"viewed":True}})
