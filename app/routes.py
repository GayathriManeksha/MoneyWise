from flask import Flask, request, flash, url_for, redirect, render_template ,json

from app import app
from app.gmailread import read
from app.takeout import read_take
from app import client
from app.database import dbval

db=client.Appsdata
category=db.categorydata
# store=db.storedata
# goals=db.set_goal

@app.route('/',methods=['GET'])
def login():
    return render_template('base.html')

@app.route('/home',methods=['GET'])
def home():
    read()
    # print(goals)
    d=dbval()
    # print(d)
    # d=dict()
    # for x in g:
    #     goal_amt=int(x['goalval'])
    #     goal_cat=x['cat_name']
    #     print(goal_cat)
    #     c=category.find_one({"cat_name":goal_cat})
    #     if c!=None:
    #         print(c)
    #         d[goal_cat]=round(((goal_amt-c['Amount'])/goal_amt)*100)
    #     else:
    #         d[goal_cat]=0
    # print(d)
    dict=json.dumps(d)
    return render_template('index.html',dict=dict)

@app.route('/takeout',methods=['GET'])
def takeout():
    df=read_take()
    df2=df.groupby('Type')['Amount'].sum()
    df3=df.groupby('Name')['Amount'].sum()
    print(df2)
    print(df3)

    df4=df.groupby('Name').size().sort_values(ascending=False)
    print(df4)
    return render_template('base.html')

@app.route('/setgoals',methods=['GET','POST'])
def setgoals():
    goals=db.set_goal
    if request.method=='POST':
        if request.form.get('food')=='food':
            print("Food",request.form['foodt'])
            goals.update_one({"cat_name":"Food"},{"$set":{"goalval":request.form['foodt']}},upsert=True)
        elif request.form.get('travel')=='travel':
            goals.update_one({"cat_name":"Travel"},{"$set":{"goalval":request.form['travelt']}},upsert=True)
            print("Travel")
        elif request.form.get('shopping')=='shopping':
            goals.update_one({"cat_name":"Shopping"},{"$set":{"goalval":request.form['shoppingt']}},upsert=True)
            print("Travel")
        elif request.form.get('services')=='services':
            goals.update_one({"cat_name":"Services"},{"$set":{"goalval":request.form['servicest']}},upsert=True)
            print("Travel")
        elif request.form.get('transfers')=='transfers':
            goals.update_one({"cat_name":"Transfers"},{"$set":{"goalval":request.form['transferst']}},upsert=True)
            print("Travel")
        elif request.form.get('health')=='health':
            goals.update_one({"cat_name":"Health"},{"$set":{"goalval":request.form['healtht']}},upsert=True)
            print("Travel")
        elif request.form.get('entertainment')=='entertainment':
            goals.update_one({"cat_name":"Entertainment"},{"$set":{"goalval":request.form['entertainmentt']}},upsert=True)
            print("Travel")
        elif request.form.get('bills')=='bills':
            goals.update_one({"cat_name":"Bills"},{"$set":{"goalval":request.form['billst']}},upsert=True)
            print("Travel")
        elif request.form.get('cafe')=='cafe':
            goals.update_one({"cat_name":"Cafe"},{"$set":{"goalval":request.form['cafet']}},upsert=True)
            print("Travel")
        elif request.form.get('beverages')=='beverages':
            goals.update_one({"cat_name":"Beverages"},{"$set":{"goalval":request.form['beveragest']}},upsert=True)
            print("Travel")
        elif request.form.get('miscellaneous')=='miscellaneous':
            goals.update_one({"cat_name":"Miscellaneous"},{"$set":{"goalval":request.form['miscellaneoust']}},upsert=True)
            print("Travel")
        else:
            print("None")
        return render_template('Set_goals.html')
    else:
        return render_template('Set_goals.html')
