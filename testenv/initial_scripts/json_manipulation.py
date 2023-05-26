import pandas as pd
import json
import bson
from bson import json_util
df = pd.read_csv("account_data.csv")
df.to_json("output2.json", indent =1, orient="records")

with open("output2.json", 'r') as jsonfile:
    data = json.loads(jsonfile.read())

for x in range(6):
    data[x]["address2"] = ""
    data[x]["address3"] = ""
    data[x]["address4"] = ""
    data[x]["shipmentProfile"] = ""
    data[x]["paymentTerm"] = ""
    if data[x]["Account Number"].isnumeric():

        data[x]["groupName"] = data[x]["Parent Account"].split(" ")[0]
        data[x]["relations"] = {
        "parentAccounts" : [
            {
                "accountName" : "NIKE MASTER", 
                "id" : "569c93b43f26c104eefe55ba", 
                "accountNumber" : "NIKE_M"
            }
        ]
    }
    else:
        data[x]["groupName"] = data[x]["Account Name"].split(" ")[0]
        data[x]["relations"] = {
        "parentAccounts" : [
            {
                "accountName" : None, 
                "id" : None, 
                "accountNumber" : None
            }
        ]
    }

    data[x]["system"] = bson.ObjectId()
    data[x]["templateId"] = bson.ObjectId()
    data[x]["organization"] = bson.ObjectId()
    data[x]["isActive"] = True

    

data_obj = json_util.dumps(data, indent=4)
#data.to_json("result_.json", indent=4)
with open("result.json", 'w') as outputfile:
    outputfile.write(data_obj)
    
    
