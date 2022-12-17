from pymongo import MongoClient
client = MongoClient('localhost', 27017)

db=client.Appsdata

category=db.categorydata
store=db.storedata
goals=db.set_goal

# print(goals)
def dbval():
    g=goals.find()
    print(g)
    d=dict()
    for x in g:
        goal_amt=int(x['goalval'])
        goal_cat=x['cat_name']
        print(goal_cat)
        c=category.find_one({"cat_name":goal_cat})
        if c!=None:
            print(c)
            d[goal_cat]=round(((c['Amount'])/goal_amt)*100)
        else:
            d[goal_cat]=1
    print(d)
    return d
# c=category.find()

