from googleapiclient.discovery import build
from datetime import date
from datetime import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
# from openpyxl import Workbook

from app import client
db=client.Appsdata

category=db.categorydata
store=db.storedata
total_amt=db.total
# Scopes of the API as defined by google
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def read():

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'app/credentials.json', SCOPES)
            creds = flow.run_local_server(port=5500,prompt='consent')
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

   
   
    service = build('gmail', 'v1', credentials=creds)
    
    model = pickle.load(open('testml/model.pkl', 'rb'))
    count_vect=pickle.load(open("testml/vectorizer.pickle", 'rb'))

    sender="Amazon Pay India <no-reply@amazonpay.in>"
    query = f"from : {sender}"

    f=True
    while f==True:

        # Retrieving messages from a given sender
        results = service.users().messages().list(userId='me',labelIds = ['INBOX'] , q = query).execute()
        messages = results.get('messages', [])

        # Getting the present time
        now = datetime.now()
        

        from datetime import date,time
        last_date=date(2022,12,15)
        last_time=time(13,56,56)
        time_str=last_time.isoformat()
        date_str=last_date.isoformat()
        # date_time_str=datetime.strptime(date_str+time_str,"%Y-%m-%d%H:%M:%S")

        date_time_str=""
        date_time_str=datetime.strptime(date_str+time_str,"%Y-%m-%d%H:%M:%S")
        # try:
        #     date_time_str=pickle.load(open('lastdt.pkl','rb'))
        # except (OSError, IOError) as e:
        #     foo = 3
        #     date_time_str=datetime.strptime(date_str+time_str,"%Y-%m-%d%H:%M:%S")

        # pickle.dump(now, open('lastdt.pkl','wb'))

        # FOR TOTAL 
        total=0
        try:
            total=pickle.load(open('total.pkl','rb'))
        except (OSError, IOError) as e:
            pickle.dump(total, open('total.pkl','wb'))

        date_time_Str=""
        if not messages:
            print ("No messages found.")
        else:
            
            for message in messages:
                print("Hey")
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                # print(msg)
                try:
                    payload=msg['payload']
                    headers=payload['headers']
                    
                    for d in headers:
                        if d['name']=='Subject':
                            subject=d['value']
                        if d['name']=='From':
                            sender=d['value']
                        if d['name']=='Date':
                            date=d['value']
                            # print(date)
                            splitted_date=date.split(" ")
                            date_Str=splitted_date[1]+splitted_date[2]+splitted_date[3]+splitted_date[4]
                            date_time_Str=datetime.strptime(date_Str,"%d%b%Y%H:%M:%S")

                    # Printing the subject, sender's email and message
                    print("Subject: ", subject)
                    print("From: ", sender)
                    splittd_msg = msg['snippet'].split(" ")
                    print(msg['snippet'])
                    # splittd_msg=subject.split(" ")
                    if date_time_Str >= date_time_str:
                        print(date)
                        print(splittd_msg)
                        i=-1
                        j=-1
                        try:
                            i=splittd_msg.index("Amount")
                            j=splittd_msg.index("₹")
                        except:
                            print("error 1")

                        if j!=-1:
                            spend=int(splittd_msg[j+1])
                            print("SPEND" , spend)
                            s=' '.join(splittd_msg[i+1:j])
                            print("Store ",s)
                            p=model.predict(count_vect.transform([s]))
                            print(p)
                            category.update_one({"cat_name":p[0]},{"$inc":{"Amount":spend}},upsert=True)
                            store.update_one({"name":s,"cat_name":p[0]},{"$inc":{"Amount":spend}},upsert=True)
                            total+=spend
                            pickle.dump(total, open('total.pkl','wb'))
                        else:
                            spend=int(splittd_msg[16][1:-3])
                            s=splittd_msg[i+1]
                            print("Store ",s)
                            print("SPEND",spend)
                            p=model.predict(count_vect.transform([s]))
                            print(type(p))
                            category.update_one({"cat_name":p[0]},{"$inc":{"Amount":spend}},upsert=True)
                            store.update_one({"name":s,"cat_name":p[0]},{"$inc":{"Amount":spend}},upsert=True)
                            total+=spend
                            pickle.dump(total, open('total.pkl','wb'))
                    else:
                        print("Exit")
                        f=False
                        break
                    # print("Message: ", body)
                    print('\n')
                except:
                    print("error")
                    pass

                