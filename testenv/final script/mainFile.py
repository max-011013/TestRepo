import json
import pandas as pd
import bson
from bson import json_util
from bson.objectid import ObjectId
#from csv_to_json import json_manipulation
import pymongo

def db_connection(connectionString):
    try:
        client = pymongo.MongoClient(connectionString)
        database = client['cevadb']
        return database
    except:
        return None
    
def json_manipulation():
    try:
        df = pd.read_csv("account_data4.csv")
        df.to_json("_result.json", indent =1, orient="records")
        pending_account_list = []
        #key_list = ["accountNumber", "accountName",]
        with open("_result.json", 'r') as jsonfile:
            data = json.loads(jsonfile.read())
        for records in data:
            if (not records.get("accountNumber") or not records.get("accountName") or not records.get("address1")
                or not records.get("city") or not records.get("country") or not records.get("zipCode") or not records.get("state") 
                or not records.get("countryCode")) :
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
                if not records.get("stateCode"):
                    records["stateCode"] = ""
                if not records.get("accountType"):
                    records["accountType"] = ""
                records["isActive"] = True
                #records["system"] = ObjectId("5649d0ce087df204a8a71638")
                #records["templateId"] = ObjectId("5649d0c9087df204a8a71636")
                #records["organization"] = ObjectId("555af07389025b2b58759bca")
                records["addedBy"] = "invoizeAutomation"

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
    except:
        print("CSV File not found")
    
#create parent account 
def create_parent_account(records,coll):
    try:
        if coll.find_one({"accountNumber":records["accountNumber"]}):
            print("Account already exist")
        else:
            records["groupName"] = records["accountNumber"].split("_")[0]
            records["relations"] = {
            "childrenAccounts" : [
            ],
            "parentAccounts" : [
                
            ]}


            records["references"] = {
                    "shipmentProfile" : [
                    ], 
                    "tariffConfig" : [
                    ], 
                    "chargeProfile" : [
                    ],
                    "docProfile" : [
                    ], 
                    "deliveryProfile" : [
                    ]
            }

            del records["parentAccount"]
            #coll = db["account_sample3"]
            coll.insert_one(records)

            
    except Exception as err:
        print(err)



#create child account 
def create_child_account(records,coll):
    try:
        if coll.find_one({"accountNumber":records["accountNumber"],"accountName":records["accountName"],"templateId":ObjectId("5649d0c9087df204a8a71636")}):
            print("Account already exist")
        else:
            records["groupName"] = records["parentAccount"].split("_")[0]
            parent = coll.find_one({"accountNumber":records["parentAccount"]},{"accountName":1,"_id":1,"accountNumber":1, "relations":1 })
            # if parent is None:
            #     raise Exception("Master Account not found")
            # if not records["Account Number"].isnumeric():
            #     raise Exception("Account Number is in wrong format")
            #print(parent)
            if parent is not None:
                records["relations"] = {
                    "childrenAccounts" : [
                    ],
                    "parentAccounts" : [
                        {
                            "accountName" : parent["accountName"], 
                            "id" : str(parent["_id"]), 
                            "accountNumber" : parent["accountNumber"]
                        }
                    ]}
                del records["parentAccount"]
                coll.insert_one(records)
                child = coll.find_one({"accountNumber" : records["accountNumber"]},{"_id":1})
                #print(child)
                child_id = str(child["_id"])
                #print(child_id)
                coll.update_one({"accountNumber":parent["accountNumber"]},{ "$push" :{
                        "relations.childrenAccounts": 
                            {    "accountName" : records["accountName"], 
                                "id" : child_id, 
                                "accountNumber" : records["accountNumber"]
                            }
                            }
                        })


            else:
                with open('accounts.json', 'r') as jsonfile:
                    data = json.loads(jsonfile.read())
                data.append(records)
                data_obj = json.dumps(data, indent = 4)
                with open('accounts.json', 'w') as jsonfile:
                    jsonfile.write(data_obj)
                print("Parent not Found")
    except Exception as err:
        print(err)


#load csv data into json object
def main():
    #connectionString = 'mongodb://mongo_invoize_uat_dev:eqedT%24FszV1es%40Qo0w8%26C9V@127.0.0.1:44719/?authSource=invoize-uat&readPreference=primary&appname=MongoDB%20Compass&ssl=false'
    #connectionString = 'mongodb://mongo_invoize_uat_dev:eqedT%24FszV1es%40Qo0w8%26C9V@localhost:44719/invoize-uat?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&authSource=invoize-uat&authMechanism=SCRAM-SHA-1&3t.uriVersion=3&3t.connection.name=UAT&3t.databases=invoize-uat&3t.alwaysShowAuthDB=true&3t.alwaysShowDBFromUserRole=true'
    #connectionString = 'mongodb://localhost:27017'
    #connectionString = 'mongodb://mongo_cevadb_uday:rMd#ujFKqW@aasgh%swFxiU@localhost:4455/?authSource=cevadb&readPreference=primary&appname=MongoDB%20Compass&ssl=false'
    #connectionString = 'mongodb://mongo_cevadb_admin@35.202.190.33:27129/?retryWrites=false&serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&authSource=cevadb&authMechanism=SCRAM-SHA-'
    connectionString = 'mongodb://mongo_cevadb_uday:rMd%23ujFKqW%40aasgh%25swFxiU@localhost:4455/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&authSource=cevadb&authMechanism=SCRAM-SHA-1'
    json_manipulation()
    db = db_connection(connectionString)
    try:
        if db is not None:
            coll = db["Account"]

            with open("_result.json", 'r') as jsonfile:
                data = json.loads(jsonfile.read())
            if data:
                for records in data:
                    #collection.find({"_id": {"$": dummy_id}})
                    #records["system"] = records["system"]["$oid"]
                    #records["templateId"] = records["templateId"]["$oid"]
                    #records["organization"] = records["organization"]["$oid"]

                    if records["parentAccount"] is None:
                        create_parent_account(records,coll)
                    else:
                        create_child_account(records,coll)

            #x = db.list_collection_names()
            #print(x)   
                coll.update_many({"addedBy" : "invoizeAutomation"},{
                    "$set" : {
                        "templateId": ObjectId("5649d0c9087df204a8a71636"),
                        "organization" : ObjectId("555af07389025b2b58759bca"),
                        "system" : ObjectId("5649d0ce087df204a8a71638")
                    }
                })    
                    
                            
            else:
                raise Exception
        else:
            print("Database connection failed")    
            
    except Exception as err:
        print(err)
    
main()