import pymongo
from bson import ObjectId
import pandas as pd
import json
connectionString = 'mongodb://localhost:27017'
client = pymongo.MongoClient(connectionString)
database = client['T1-invoize-uat']
coll = database['Account_sample3']


coll.update_many({"addedBy" : "invoizeAutomation"},{
    "$set" : {
        "templateId": ObjectId("5649d0c9087df204a8a71636"),
        "organization" : ObjectId("555af07389025b2b58759bca"),
        "system" : ObjectId("5649d0ce087df204a8a71638")
    }
})


