from pymongo import  MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, render_template,request,redirect,url_for,Markup
import os
app = Flask(__name__)
from datetime import date
import datetime
import time
client = MongoClient("mongodb+srv://ubuntuVM:vamshi81@mymongo-yiker.azure.mongodb.net/reddit?retryWrites=true&w=majority")
db = client["reddit"]


colls = db.list_collection_names()

colls.remove("subreddits")
colls.remove("users")
colls.remove("loves_DND")

colls = list(filter(lambda x: "_user" not in x,colls))


colls=sorted(colls)

searchTerm=''
isVid=False
byLikes=False

collection=''

rdts=[]
days=''

@app.route("/scan")
def scanAgain():

    os.system("python3 main.py &")
    return "please wait 3 mins"



@app.route("/addLove",methods=["POST","GET"])
def addFav():
    collectionNamee =  request.args.get("collectionName")

    try:
        val = list(db["loves_DND"].find({"_id":collectionNamee }))[0]["value"]
    except Exception as e:
        val=0
        db["loves_DND"].insert_one({"_id":collectionNamee,"value":val})
        
    db["loves_DND"].update_one({"_id":collectionNamee},{"$set":{"value":val+1}})

    print("added to fav")

    return redirect(url_for('fload'))


@app.route("/add")
def addCollection():

    rd=request.args.get("collection")
    user =request.args.get("user")
    if rd :
        url = "https://www.reddit.com/r/"+rd+"/"
        try:
            db["subreddits"].insert_one({"_id":url})
            return url+" added"
        except Exception as e:
            return str(e)
    if user :
        try:
            db["users"].insert_one({"_id":user,"viewed":False})
            return user+" added"
        except Exception as e:
            return str(e)
        

@app.route("/fload")
def fload():

    rd = rdts.pop(0)

    collectionName = rd["collectionname"]

    print(collectionName)
    print("id",rd["_id"])

    db[collectionName].update_one({"_id":rd["_id"]},{"$set":{"viewed":True}})

    return render_template("display.html",rd=rd,left=len(rdts),date=str(date.fromtimestamp(int(rd["timestamp"]))))




@app.route("/load")
def load():
    global rdts
    rdts=[]

    global collection
    global days

    print("load",collection)
    startDate=endDate=''

    if days:
        endDate = int(time.mktime(datetime.datetime.strptime(str(datetime.date.today()-datetime.timedelta(days=-1)),"%Y-%m-%d").timetuple()))
        startDate = int(time.mktime(datetime.datetime.strptime(str(datetime.date.today()-datetime.timedelta(days=int(days)+1)),"%Y-%m-%d").timetuple()))


    if collection == "":
        print("All collections",len(colls))
        if searchTerm !="" :
            for ct in colls:
                if not isVid:
                    tmrds=list(db[ct].find({"viewed":False}))
                else:
                    tmrds=list(db[ct].find({"viewed":False,"isvid":True}))
                for rd in tmrds:
                    if searchTerm.lower() in rd["title"].lower():
                        rdts.append(rd)
        else:
            for ct in colls:
                if isVid:
                    rdts.extend(list(db[ct].find({"viewed":False,"isvid":True})))
                else:
                    rdts.extend(list(db[ct].find({"viewed":False})))
    else:
        print("else",collection)
        if "tier" in collection:
            collections = list(map(lambda x:x["_id"],db[collection].find({})))
            for collection in collections:
                if searchTerm :
                    if not isVid:
                        tmrds=list(db[collection].find({"viewed":False}))
                    else:
                        tmrds=list(db[collection].find({"viewed":False,"isvid":True}))
                    for rd in tmrds:
                        if searchTerm.lower() in rd["title"].lower():
                            rdts.append(rd)
                else:
                    if isVid:
                        rdts.extend(list(db[collection].find({"viewed":False,"isvid":True})))
                    else:
                        rdts.extend(list(db[collection].find({"viewed":False})))
        else:

            if searchTerm :
                if not isVid:
                    tmrds=list(db[collection].find({"viewed":False}))
                else:
                    tmrds=list(db[collection].find({"viewed":False,"isvid":True}))
                for rd in tmrds:
                    if searchTerm.lower() in rd["title"].lower():
                        rdts.append(rd)
            else:
                if isVid:
                    rdts.extend(list(db[collection].find({"viewed":False,"isvid":True})))
                else:
                    rdts.extend(list(db[collection].find({"viewed":False})))


    if startDate:
        tmppp=[]
        for twt in rdts:
            if int(twt["timestamp"]) >= startDate and int(twt["timestamp"]) <= endDate:
                tmppp.append(twt)
        rdts=tmppp

    if byLikes == "likes":
        rdts=sorted(rdts,key=lambda x: x["votes"],reverse=True)
    elif byLikes == "date":
        rdts=sorted(rdts,key=lambda x: x["timestamp"],reverse=True)
    else:
        rdts=sorted(rdts,key=lambda x: x["numComments"],reverse=True)

    return redirect(url_for('fload'))    


@app.route("/reboot")
def maston():
    os.system("sh reboot.sh consumer.py "+str(os.getpid())+" &")


    return render_template('index.html',collections=colls)


@app.route("/mainpage",methods=["POST","GET"])
def mainpage():

    global searchTerm
    global isVid
    global byLikes
    global collection 

    global days

    searchTerm = request.args.get("searchkey")

    isVid = request.args.get("file") == "vid"

    byLikes = request.args.get("sort")

    collection =  request.args.get("collection")

    days = request.args.get("days")

    print(collection)

    return redirect(url_for('load'))













@app.route("/")
def main():
    return render_template("index.html",collections=colls)

if __name__ == '__main__':
    app.run('0.0.0.0',port=8000)