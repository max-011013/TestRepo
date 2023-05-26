import json
import pymongo

CONNECTION_STRING = "mongodb+srv://<username>:<password >@cluster0.qzfhccj.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECTION_STRING)

with open("result.json", 'r') as jsonfile:
    data = json.loads(jsonfile.read())

dbname = client['account_sample']
coll = dbname['Account_S']

for x in range(6):
    coll.insert_one(data[x])
