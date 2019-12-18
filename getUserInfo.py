import requests
from fake_headers import Headers
from pymongo import  MongoClient
from pymongo.errors import DuplicateKeyError


client = MongoClient("localhost")
db = client["reddit"]



def scrap(url,headers):

    print(url)
    strCollection = url.split("/user/")[-1].split("/")[0]

    strCollection = strCollection+"_user"

    collection = db[strCollection]

    rjson = requests.get(url,headers=headers)
    json = rjson.json()

    posts = json["data"]["children"]

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
            postData["_id"]=post["id"]
            postData["viewed"]=False
            postData["collectionname"]=strCollection

            if "gfycat" in post["url"]:
                postData["isvid"] = True
                postData["vidurl"] =post["media"]["oembed"]["thumbnail_url"]
            else:
                postData["isvid"] =False

            try:
                collection.insert_one(postData)
                print(postData)
            except DuplicateKeyError as e:
                print("key Error")

        except Exception as e:
            print(e)





def startsHere():

    header = Headers()

    uheaders = header.generate()

    users = list(map(lambda  x:x["_id"],db["users"].find({"viewed":False})))


    url = "https://www.reddit.com/user/"

    for usr in users:
        try:
            nurl = url+usr+"/.json?limit=1000"
            scrap(nurl,uheaders)
        except Exception as e:
            e=0
        db["users"].update_one({"_id":usr},{"$set":{"viewed":True}})

if __name__ == '__main__':
    startsHere()