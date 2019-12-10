from pymongo import  MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, render_template,request,redirect,url_for,Markup
import os
app = Flask(__name__)
from datetime import date

client = MongoClient("localhost")
db = client["reddit"]


colls = db.list_collection_names()

colls.remove("subreddits")

searchTerm=''
isVid=False
byLikes=False

collection=''

rdts=[]


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


    print("load",collection)

    if collection == "":
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


    if byLikes:
        rdts=sorted(rdts,key=lambda x: x["votes"],reverse=True)
    else:
        rdts=sorted(rdts,key=lambda x: x["timestamp"],reverse=True)

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

    searchTerm = request.args.get("searchkey")

    isVid = request.args.get("file") == "vid"

    byLikes = request.args.get("sort") == "likes"

    collection =  request.args.get("collection")

    print(collection)

    return redirect(url_for('load'))













@app.route("/")
def main():
    return render_template("index.html",collections=colls)

if __name__ == '__main__':
    app.run('0.0.0.0',port=8000)