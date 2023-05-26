import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017')
database = client['Accountsample']
coll = database['Accounts']

coll.delete_one({"Account Number" :"Test1_M"})