from flask import Flask, request, flash, url_for, redirect, render_template ,json

from app import app
from app.gmailread import read
from app.takeout import read_take
# from app import client
from pymongo import MongoClient
from app.database import dbval
import pickle
from pandas import DataFrame
# from werkzeug.utils import secure_filename
import os

client = MongoClient('mongodb://172.17.0.2:27017/')
db=client.Appsdata
db2=client.testdb
monthly=db2.monthlydb
total_amt=db.total
# store=db.storedata
# goals=db.set_goal

@app.route('/',methods=['GET'])
def login():
    return render_template('Login_Page.html')

@app.route('/home',methods=['POST'])
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
    data=monthly.find()
    print(data)
    # tot_amt=total_amt.find_one()
    # print(total_amt['Amount'])
    totalout=0
    goals=db.set_goal
    gl=goals.find()
    for g in gl:
        totalout+=int(g['goalval'])
    print(totalout)
    total=pickle.load(open('total.pkl','rb'))
    print("TOTAL ",type(total),total)
    tot_per=round(total*100/totalout)+1
    months=[]
    values=[]
    for x in data:
        print(x)
        months.append(x['Month'])
        values.append(x['Total'])
    print(months)
    print(values)
    m=json.dumps(months)
    v=json.dumps(values)
    dict=json.dumps(d)
    t=json.dumps(tot_per)
    ttl=json.dumps(total)
    ttlo=json.dumps(totalout)
    return render_template('index.html',dict=dict,months=m,values=v,tot=t,Total=ttl,Totalout=ttlo)

@app.route('/takeout',methods=['POST','GET'])
def takeout():
    df=read_take()
    df2=df.groupby('Type')['Amount'].sum()
    # df3=df.groupby('Name')['Amount'].sum()
    # df4=df.groupby('Name').size().sort_values(ascending=False)
    # print(df4)
    # print(df2)
    print(df2)
    cat=[]
    val=[]
    df4=df.groupby('Name').size().sort_values(ascending=False)
    print(df4.iloc[0])
    if request.method=='POST':
        # if 'file' not in request.files:
        #     flash('No file')
        #     return redirect(request.url)

        # file = request.files['file']
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)

        # if file:
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], "My Activity.html"))
        
        for items in df2.iteritems():
            cat.append(items[0])
            val.append(items[1])
        c=json.dumps(cat)
        a=json.dumps(val)
        return render_template('page.html',cat=c,val=a)
    return render_template('page.html',cat=cat,val=val)

@app.route('/setgoals',methods=['POST','GET'])
def setgoals():
    d=dict()
    catg=["Food", "Travel", "Shopping", "Services", "Transfers","Health","Entertainment","Bills","Cafe","Beverages","Miscellaneous"]
    for c in catg:
        d[c]='0'
    goals=db.set_goal
    gl=goals.find()
    for g in gl:
        d[g['cat_name']]=g['goalval']
    if request.method=='POST':
        if request.form.get('food')=='food':
            print("Food",request.form['foodt'])
            # x=goals.find_one({"cat_name":"Food"})
            # if  x!=None:
            #     d['Food']=x['goalval']
            # else:
            #     d['Food']='0'
            goals.update_one({"cat_name":"Food"},{"$set":{"goalval":request.form['foodt']}},upsert=True)
        elif request.form.get('travel')=='travel':
            # x=goals.one({"cat_name":"Travel"})
            # if  x!=None:
            #     d['Travel']=x['goalval']
            # else:
            #     d['Travel']=0
            goals.update_one({"cat_name":"Travel"},{"$set":{"goalval":request.form['travelt']}},upsert=True)
            print("Travel")
        elif request.form.get('shopping')=='shopping':
            # x=goals.find_one({"cat_name":"Shopping"})
            # if  x!=None:
            #     d['shopping']=x['goalval']
            # else:
            #     d['shopping']='0'
            goals.update_one({"cat_name":"Shopping"},{"$set":{"goalval":request.form['shoppingt']}},upsert=True)
            print("Travel")
        elif request.form.get('services')=='services':
            # x=goals.find_one({"cat_name":"Services"})
            # if  x!=None:
            #     d['Services']=x['goalval']
            # else:
            #     d['Services']='0'
            goals.update_one({"cat_name":"Services"},{"$set":{"goalval":request.form['servicest']}},upsert=True)
            print("Travel")
        elif request.form.get('transfers')=='transfers':
            # x=goals.find_one({"cat_name":"Transfers"})
            # if  x!=None:
            #     d['Transfers']=x['goalval']
            # else:
            #     d['Transfers']='0'
            goals.update_one({"cat_name":"Transfers"},{"$set":{"goalval":request.form['transferst']}},upsert=True)
            print("Travel")
        elif request.form.get('health')=='health':
            # x=goals.find_one({"cat_name":"Health"})
            # if  x!=None:
            #     d['Health']=x['goalval']
            # else:
            #     d['Health']='0'
            goals.update_one({"cat_name":"Health"},{"$set":{"goalval":request.form['healtht']}},upsert=True)
            print("Travel")
        elif request.form.get('entertainment')=='entertainment':
            # x=goals.find_one({"cat_name":"Entertainment"})
            # if  x!=None:
            #     d['Entertainment']=x['goalval']
            # else:
            #     d['Entertainment']='0'
            goals.update_one({"cat_name":"Entertainment"},{"$set":{"goalval":request.form['entertainmentt']}},upsert=True)
            print("Travel")
        elif request.form.get('bills')=='bills':
            # x=goals.find_one({"cat_name":"Bills"})
            # if  x!=None:
            #     d['Bills']=x['goalval']
            # else:
            #     d['Bills']='0'
            goals.update_one({"cat_name":"Bills"},{"$set":{"goalval":request.form['billst']}},upsert=True)
            print("Travel")
        elif request.form.get('cafe')=='cafe':
            # x=goals.find_one({"cat_name":"Cafe"})
            # if  x!=None:
            #     d['Cafe']=x['goalval']
            # else:
            #     d['Cafe']='0'
            goals.update_one({"cat_name":"Cafe"},{"$set":{"goalval":request.form['cafet']}},upsert=True)
            print("Travel")
        elif request.form.get('beverages')=='beverages':
            # x=goals.find_one({"cat_name":"Food"})
            # if  x!=None:
            #     d['Beverages']=x['goalval']
            # else:
            #     d['Beverages']='0'
            goals.update_one({"cat_name":"Beverages"},{"$set":{"goalval":request.form['beveragest']}},upsert=True)
            print("Travel")
        elif request.form.get('miscellaneous')=='miscellaneous':
            # x=goals.find_one({"cat_name":"Food"})
            # if  x!=None:
            #     d['Miscellaneous']=x['goalval']
            # else:
            #     d['Miscellaneous']='0'
            goals.update_one({"cat_name":"Miscellaneous"},{"$set":{"goalval":request.form['miscellaneoust']}},upsert=True)
            print("Travel")
        else:
            print("None")
        print(d)
        return render_template('Set_goals.html',dict=d)
    return render_template('Set_goals.html',dict=d)

@app.route('/report',methods=['GET','POST'])
def report():
    category=db.categorydata
    cat=category.find()
    ctg=[]
    amt=[]
    for x in cat:
        ctg.append(x['cat_name'])
        amt.append(x['Amount'])
    # print(months)
    # print(values)
    # list_cur = list(cat)
    # dfc = DataFrame(list_cur)
    # print(dfc.head())
    # df2c=dfc.groupby('cat_name')['Amount'].sum().sort_values(ascending=False)
    # # df3=df2.to_frame()
    # df2tc=df2c.reset_index()
    # print(df2tc.iloc[0])

    # # Use DataFrame.groupby() and Size() 
    # df4c=dfc.groupby('Name').size() .sort_values(ascending=False)
    # df5c=df4c.reset_index()
    # print("Highest frequency payment",df5c.iloc[0].Name)
    c=json.dumps(ctg)
    a=json.dumps(amt)
    return render_template('report.html',category=c,amount=a)