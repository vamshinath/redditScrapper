import requests
from fake_headers import Headers
from pymongo import  MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient("localhost")
db = client["reddit2"]
import datetime

from getFileSize import getFileSize

def scrap(url,ourl,headers,strCollection):


    print(strCollection)

    collection = db[strCollection]


    idss = list(map(lambda  x:x["_id"],collection.find({})))


    rjson = requests.get(url,headers=headers)
    json = rjson.json()

    posts = json["data"]["children"]

    try:
        ext = list(db["subreddits"].find({"_id":url}))
        health = int(ext[0]["health"])
    except Exception as e:
        health=1
        print(e)


    for post in posts:
        try:
            post = post["data"]

            postData={}
            postData["title"] = post["title"]
            postData["subreddit"]=post["subreddit"]
            postData["votes"]=post["ups"]
            postData["score"] = post["score"]
            postData["timestamp"]=post["created"]
            postData["url"]=post["url"]
            postData["author"]=post["author"]

            

            try:
                grouper = datetime.datetime.fromtimestamp(int(post["created"]))
                grouper = str(grouper.date())
            except Exception as e:
                grouper = "1"
            postData["group"]=grouper
            
            try:
                o18  = post["over_18"]
                postData["numComments"]=int(post["num_comments"])
            except Exception as e:
                o18=False
                
            postData["over18"] = o18
            postData["_id"]=post["id"]
            postData["viewed"]=False
            postData["collectionname"]=strCollection

            post["isVid"] = post["is_video"]

            try:
                

                if not postData["_id"] in idss:
                    try:
                        flsz = getFileSize(post["url"])
                    except Exception as e:
                        flsz = -1
                    postData["flsz"]=flsz

                    collection.insert_one(postData)
                    db["subreddits"].update_one({"_id":ourl},{"$set":{"lastUpdated":datetime.datetime.now()}})
                    db["subreddits"].update_one({"_id":ourl},{"$set":{"health":health+1}})
                    print(postData)
                else:
                    db["subreddits"].update_one({"_id":ourl},{"$set":{"health":health-1}})

            except DuplicateKeyError as e:
                print("key Error")

        except Exception as e:
            print(e)

def startsHere():

    header = Headers()
    uheaders = header.generate()

    #scrap("https://www.reddit.com/r/JacquelineFernandez/new.json?limit=1000",uheaders,"jacq")

    urls = list(map(lambda  x:x["_id"],db["subreddits"].find({"active":True})))

    turls={}
    for url in urls:
        if len(url) < 1:
            continue
        strCollection = url.split("/r/")[-1].split("/")[0]
        print(strCollection)
        collection = db[strCollection]
        try:
            nele=len(list(collection.find({})))
        except Exception as e:
            nele=0
        turls[url]=[nele,strCollection]

    urls = sorted(turls.items(),key=lambda x: x[1][0])

    for url,x in urls:
        try:
            print(url)
            ourl=url
            url = url+"new.json?limit=1000"
            scrap(url,ourl,uheaders,x[1])
        except Exception as e:
            print(e)
            

if __name__ == '__main__':
    startsHere()
