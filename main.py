import requests
from fake_headers import Headers
from pymongo import  MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient("localhost")
db = client["reddit"]
import datetime


def scrap(url,headers,ourl):

    strCollection = url.split("/r/")[-1].split("/")[0]

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
                o18  = post["over_18"]
                postData["numComments"]=int(post["num_comments"])
            except Exception as e:
                o18=False
                
            postData["over18"] = o18
            try:
                db["users"].insert_one({"_id":post["author"],"viewed":False})
            except Exception as e:
                e=0
            postData["_id"]=post["id"]
            postData["viewed"]=False
            postData["collectionname"]=strCollection

            if "gfycat" in post["url"]:
                postData["isvid"] = True
                postData["vidurl"] =post["media"]["oembed"]["thumbnail_url"].replace("size_restricted.gif","mobile.mp4")

            else:
                postData["isvid"] =False


            try:
                
                if not postData["_id"] in idss:
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

    urls = list(map(lambda  x:x["_id"],db["subreddits"].find({})))

    turls={}
    for url in urls:
        strCollection = url.split("/r/")[-1].split("/")[0]
        collection = db[strCollection]
        try:
            nele=len(list(collection.find({})))
        except Exception as e:
            nele=0
        turls[url]=nele

    urls = sorted(turls.items(),key=lambda x: x[1])

    for url,_ in urls:
        try:
            print(url)
            ourl=url
            url = url+"new.json?limit=1000"
            scrap(url,uheaders,ourl)
        except Exception as e:
            print(e)
            

if __name__ == '__main__':
    startsHere()
