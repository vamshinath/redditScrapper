from pymongo import  MongoClient
import sys,re
from prettytable import PrettyTable

client = MongoClient("localhost")
db = client["reddit"]

urls = list(map(lambda  x:x["_id"],db["subreddits"].find({})))
    
table = PrettyTable()

words = {}
nowords=["this","with","like","your","want","have","some","just","would"]

with open("noWords.txt","r") as fl:
    for ln in fl:
        nowords.append(ln[:-1])

for url in urls:
    strCollection = url.split("/r/")[-1].split("/")[0]
    collection = db[strCollection]
    try:
        nele=list(collection.find({"viewed":False}))
        for rd in nele:
            title = list(filter(lambda x: len(re.sub("[^a-z]",'',x.lower())) > 3,rd["title"].split()))
            for tl in title:
                tl = re.sub("[^a-z]",'',tl.lower())
                if tl in nowords:
                    continue
                words[tl]=words.get(tl,0)+1
    except Exception as e:
        nele=0
words=sorted(words.items(),key=lambda x: x[1],reverse=True)

ctr=0
nowordlist=[]
table.field_names=["keyWord","times"]
for wd,tim in words:
    if tim < 100:
        continue
    table.add_row([wd,tim])
    # ch = input("Press Enter for to register noWord/break/*ignore:")
    # if ch == "break":
    #     break
    # elif ch == "":
    #     nowordlist.append(wd)

print(table)

with open("noWords.txt","a") as fl:
    for wd in nowordlist:
        fl.write(wd+"\n")
    