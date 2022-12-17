from app import client

db=client.Appdata

category=db.categorydata
store=db.storedata

category.update_one({"cat_name":"Health"},{"$inc":{"Amount":50}},upsert=True)
store.update_one({"name":"Anan Medicals","cat_name":"Health"},{"$inc":{"Amount":50}},upsert=True)

