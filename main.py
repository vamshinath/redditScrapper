import requests
from fake_headers import Headers
from pymongo import  MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient("localhost")
db = client["reddit"]



def scrap(url,headers):

    strCollection = url.split("/r/")[-1].split("/")[0]

    print(strCollection)

    collection = db[strCollection]


    idss = list(map(lambda  x:x["_id"],collection.find({})))


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
                if not postData["_id"] in idss:
                    collection.insert_one(postData)
                    print(postData)
            except DuplicateKeyError as e:
                print("key Error")

        except Exception as e:
            print(e)



def startsHere():

    header = Headers()

    uheaders = header.generate()

    urls = list(map(lambda  x:x["_id"],db["subreddits"].find({})))

    for url in urls:
        print(url)
        url = url+"new.json?limit=1000"
        scrap(url,uheaders)

if __name__ == '__main__':
    startsHere()
