import json
import pandas as pd
import bson
from bson import json_util
#from csv_to_json import json_manipulation
import pymongo

def db_connection():
    try:
        client = pymongo.MongoClient('mongodb://localhost:27017')
        database = client['invoize-uat']
        return database
    except:
        return None
    
def json_manipulation():
    df = pd.read_csv("account_data.csv")
    df.to_json("_result.json", indent =1, orient="records")
    pending_account_list = []
    with open("_result.json", 'r') as jsonfile:
        data = json.loads(jsonfile.read())
    for records in data:
        if (not records.get("Account Number") or not records.get("Account Name") or not records.get("Address1")
            or not records.get("City") or not records.get("Country name") or not records.get("Zip Code") or not records.get("State") 
            or not records.get("Country Code") ):
            pending_account_list.append(records)
            #print("Records in if")
            #print(records)
            #data.remove(records)
        else:
            #print(records)
            if not records.get("address2"):
                records["address2"] = ""
            if not records.get("address3"):
                records["address3"] = ""
            if not records.get("address4"):
                records["address4"] = ""
            if not records.get("address4"):
                records["shipmentProfile"] = ""
            if not records.get("address4"):
                records["paymentTerm"] = ""
            records["system"] = bson.ObjectId("5649d0ce087df204a8a71638")
            records["templateId"] = bson.ObjectId("5649d0c9087df204a8a71636")
            records["organization"] = bson.ObjectId("555af07389025b2b58759bca")
            records["isActive"] = True

    for records in pending_account_list:
        data.remove(records)
    #to overcome below error we used json_util    
    #TypeError: Object of type type is not JSON serializable
    data_obj = json_util.dumps(data, indent=4)
    #data.to_json("result_.json", indent=4)
    #print(data)
    with open("_result.json", 'w') as outputfile:
        outputfile.write(data_obj)
    missing_accounts = json.dumps(pending_account_list, indent = 4)
    with open("accounts.json",'w') as jfile:
        jfile.write(missing_accounts)

    
#create parent account 
def create_parent_account(records,coll):
    try:
        if coll.find_one({"Account Number":records["Account Number"]}):
            print("Account already exist")
        else:
            records["groupName"] = records["Account Name"].split(" ")[0]
            records["relations"] = {
            "childrenAccounts" : [
            ],
            "parentAccounts" : [
                {
                    "accountName" : None, 
                    "id" : None, 
                    "accountNumber" : None
                }
            ]}
            del records["Parent Account"]
            #coll = db["account_sample3"]
            coll.insert_one(records)
    except:
        print("Database Error")



#create child account 
def create_child_account(records,coll):
    if coll.find_one({"Account Number":records["Account Number"]}):
        print("Account already exist")
    else:
        records["groupName"] = records["Parent Account"].split(" ")[0]
        parent = coll.find_one({"Account Number":records["Parent Account"]},{"Account Name":1,"_id":1,"Account Number":1 })
        # if parent is None:
        #     raise Exception("Master Account not found")
        # if not records["Account Number"].isnumeric():
        #     raise Exception("Account Number is in wrong format")
        print(parent)
        print(type(parent))
        if parent is not None and records["Account Number"].isnumeric():
            records["relations"] = {
                 "childrenAccounts" : [
                ],
                "parentAccounts" : [
                    {
                        "accountName" : parent["Account Name"], 
                        "id" : parent["_id"], 
                        "accountNumber" : parent["Account Number"]
                    }
                ]}
            
            coll.insert_one(records)
            relation_dict = {}
            child = coll.find({"Account Number":records["Parent Account"]},{"Account Name":1,"_id":1,"Account Number":1 })
            p1 = coll.find({"Account Number":records["Parent Account"]},{"Account Name":1,"_id":1,"Account Number":1 })




            coll.update_one({"Account Number":records["Parent Account"]},{ "$set" :{
                "relations" : relation_dict
                }}
            )
        else:
            with open('accounts.json', 'r') as jsonfile:
                data = json.loads(jsonfile.read())
            data.append(records)
            data_obj = json.dumps(data, indent = 4)
            with open('accounts.json', 'w') as jsonfile:
                jsonfile.write(data_obj)
            print("Parent not Found")



#load csv data into json object
def main():
    json_manipulation()
    db = db_connection()
    if db is not None:
        coll = db["account_sample6"]
        with open("_result.json", 'r') as jsonfile:
            data = json.loads(jsonfile.read())
        if data:
            for records in data:
                records["system"] = records["system"]["$oid"]
                records["templateId"] = records["templateId"]["$oid"]
                records["organization"] = records["organization"]["$oid"]
                child = coll.find({"Account Number":records["Parent Account"]},{"_id":1})
                for x in child:
                    print(x)
                    print(type(x))
                if records["Parent Account"] is None:
                    create_parent_account(records,coll)
                else:
                    create_child_account(records,coll)
            

                    
        else:
            print("File is empty")
    else:
        print("Database connection failed")

    
main()