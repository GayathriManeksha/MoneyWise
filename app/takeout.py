# Importing BeautifulSoup and
# it is in the bs4 module
from bs4 import BeautifulSoup
import html_to_json
import nltk
from nltk.tokenize import word_tokenize
import pandas as pd
import spacy 
from string import punctuation
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from pymongo import MongoClient
# from bson.objectid import ObjectId
# import seaborn as sns
from app import client

# def get_hotwords(text):
#         result = []
#         pos_tag = ['NOUN'] 
#         doc = nlp(text.lower()) 
#         for token in doc:
#             if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
#                 continue
#             if(token.pos_ in pos_tag):
#                 result.append(token.text)
#         return result
def read_take():
    nlp = spacy.load("en_core_web_sm")
    db=client.Appsdata
    dbdata= db.data
    shopfreq=db.freq
    HTMLFileToBeOpened = open("app/My Activity.html", "r")

    # Reading the file and storing in a variable
    contents = HTMLFileToBeOpened.read()

    # print(contents)
    # Creating a BeautifulSoup object and
    # specifying the parser
    soupText = BeautifulSoup(contents, 'html.parser')
    data = '' 
    list1=[]
    list2=[]
    list3=[]
    model = pickle.load(open('testml/model.pkl', 'rb'))
    count_vect=pickle.load(open("testml/vectorizer.pickle", 'rb'))

    for data in soupText.find_all("div",class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"): 
        txt=data.get_text()
        x=word_tokenize(txt)
        # print(x)
        if x[0] =="Paid" and x[2]=="to":
            # print(x[1])
            y=int(x[1][3:-3].replace(',',''))
            # print(y)
            i=-1
            try:
                i=x.index("using")
            except ValueError:
                r=1
            if i!=-1:
                # print(x[3:i])
                s=' '.join(x[3:i])
                # print(s)
                p=model.predict(count_vect.transform([s]))
                # print(p)
                list1.append(s)
                list2.append(y)
                list3.append(p[0])
    data={'Name':list1,'Type':list3,'Amount':list2}

    df=pd.DataFrame(data) 
    df2=df.groupby('Type')['Amount'].sum()
    df3=df.groupby('Name')['Amount'].sum()

    df4=df.groupby('Name').size().sort_values(ascending=False)
    print(df4)


    try:
        id=0
        for items in df4.iteritems():
            shopfreq.insert_one({'_id':id,'Store':items[0], 'Count':items[1]})
            id=id+1
    except:
        print("Duplicate")

    try:
        id=0
        for items in df2.iteritems():
            dbdata.insert_one({'_id':id,'Category':items[0], 'Sum':items[1]})
            id=id+1
    except:
        print("Duplicate")
