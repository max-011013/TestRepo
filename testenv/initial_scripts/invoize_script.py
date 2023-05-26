import json
from csv_to_json import json_manipulation
import pymongo

def db_connection():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    database = client['Accountsample3']
    return database
#create parent account 
def create_parent_account(records,db):
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
    coll = db["Accounts"]
    coll.insert_one(records)



#create child account 
def create_child_account(records,db):
    coll = db["Accounts"]
    records["groupName"] = records["Parent Account"].split(" ")[0]
    parent = coll.find_one({"Account Number":records["Parent Account"]},{"_id":1,"Account Number":1,"Account Name":1 })
    if parent is None:
        raise Exception("Master Account not found")
    if not records["Account Number"].isnumeric():
        raise Exception("Account Number is in wrong format")
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



#load csv data into json object
def main():
    json_manipulation()
    db = db_connection()
    #coll = db["accounts"]
    with open("_result.json", 'r') as jsonfile:
        data = json.loads(jsonfile.read())
    if data:
        for records in data:
            records["system"] = records["system"]["$oid"]
            records["templateId"] = records["templateId"]["$oid"]
            records["organization"] = records["organization"]["$oid"]

            if records["Parent Account"] is None:
                create_parent_account(records,db)
            else:
                create_child_account(records,db)
    else:
        raise Exception("File is empty")

    
main()