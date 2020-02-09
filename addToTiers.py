from pymongo import  MongoClient
from pymongo.errors import DuplicateKeyError
import webbrowser
client = MongoClient("localhost")
db = client["reddit"]


colls = db.list_collection_names()

colls.remove("subreddits")
colls.remove("users")
colls.remove("loves_DND")

colls = list(filter(lambda x: "_user" not in x,colls))


tierDbs = list(filter(lambda x:"tier" in x,colls))

trecs=[]
for tr in tierDbs:
    #print(list(db[tr].find({})))
    trecs.extend(list(map(lambda x:x["_id"],db[tr].find({}))))


colls = list(filter(lambda x:"tier" not in x and x not in trecs,colls ))

for ct in colls:
    url = "https://www.reddit.com/r/{}/".format(ct)
    webbrowser.open_new_tab(url)
    tr=input("Enter t(1_ind_act_special/2_specific_act/3_porn_act/4_porn/5_body_parts/6_safe/7_porn_special):")
    if tr == "":
        db.drop_collection(ct)
        continue
    tr="tier"+tr
    try:
        db[tr].insert_one({"_id":ct})
    except DuplicateKeyError as e:
        print(e)

