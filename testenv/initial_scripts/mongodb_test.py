import pymongo
import json
import bson

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['test-db']


#with open("result2.json", 'r') as jsonfile:
#    data = json.loads(jsonfile.read())

#for x in range(6):
#    data[x]["system"] = data[x]["system"]["$oid"]
#    data[x]["templateId"] = data[x]["templateId"]["$oid"]
#    data[x]["organization"] = data[x]["organization"]["$oid"] 
coll = db['Accountsample5']


with open("test.json", 'r') as jsonfile:
    data = json.loads(jsonfile.read())
for records in data:
    records["system"] = records["system"]["$oid"]
    records["templateId"] = records["templateId"]["$oid"]
    records["organization"] = records["organization"]["$oid"]
    if records["Account Number"].isnumeric():
        records["groupName"] = records["Parent Account"].split(" ")[0]
        parent = coll.find_one({"Account Number":records["Parent Account"]},{"_id":1,"Account Number":1,"Account Name":1 })
        print(parent)
        if parent is None:
            print("Master Account not found")
            break
        else:
            records["relations"] = {
            "parentAccounts" : [
                {
                    "accountName" : parent["Account Name"], 
                    "id" : parent["_id"], 
                    "accountNumber" : parent["Account Number"]
                }
            ]}
            coll.insert_one(records)
    else:
        records["groupName"] = records["Account Name"].split(" ")[0]
        records["relations"] = {
        "parentAccounts" : [
            {
                "accountName" : None, 
                "id" : None, 
                "accountNumber" : None
            }
        ]}
        del records["Parent Account"]
        coll.insert_one(records)


