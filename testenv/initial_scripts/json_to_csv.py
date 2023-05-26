import json
import pandas as pd

account_data = [
    { 
    "_id" : "5702471a94dc36043043676d", 
    "city" : "", 
    "system" : "5649d0ce087df204a8a71638", 
    "countryCode" : "US", 
    "accountNumber" : "7574876", 
    "address1" : "", 
    "address2" : "", 
    "address3" : "", 
    "address4" : "", 
    "zipCode" : "", 
    "accountName" : "NIKE INC C/O IRONDATA", 
    "state" : "", 
    "stateCode" : "", 
    "accountType" : "International", 
    "country" : "United State", 
    "organization" : "555af07389025b2b58759bca", 
    "isActive" : True, 
    "templateId" : "5649d0c9087df204a8a71636", 
    "relations" : {
        "parentAccounts" : [
            {
                "accountName" : "NIKE MASTER", 
                "id" : "569c93b43f26c104eefe55ba", 
                "accountNumber" : "NIKE_M"
            }
        ]
    }, 
    "shipmentProfile" : "", 
    "paymentTerm" : 30.0, 
    "groupName" : "Nike"
},
{ 
    "_id" : "5702471a94dc36043043676c", 
    "city" : "", 
    "system" : "5649d0ce087df204a8a71638", 
    "countryCode" : "US", 
    "accountNumber" : "1000298743", 
    "address1" : "", 
    "address2" : "", 
    "address3" : "", 
    "address4" : "", 
    "zipCode" : "", 
    "accountName" : "NIKE INC", 
    "state" : "", 
    "stateCode" : "", 
    "accountType" : "International", 
    "country" : "United State", 
    "organization" : "555af07389025b2b58759bca", 
    "isActive" : True, 
    "templateId" : "5649d0c9087df204a8a71636", 
    "relations" : {
        "parentAccounts" : [
            {
                "accountName" : "NIKE MASTER", 
                "id" : "569c93b43f26c104eefe55ba", 
                "accountNumber" : "NIKE_M"
            }
        ]
    }, 
    "shipmentProfile" : "", 
    "paymentTerm" : 0.0, 
    "groupName" : "Nike"
},
{ 
    "_id" : "5702472a94dc360430436c0f", 
    "city" : "", 
    "system" : "5649d0ce087df204a8a71638", 
    "countryCode" : "US", 
    "accountNumber" : "3058449", 
    "address1" : "", 
    "address2" : "", 
    "address3" : "", 
    "address4" : "", 
    "zipCode" : "", 
    "accountName" : "TRIANGLE CHRYSLER PONCE", 
    "state" : "", 
    "stateCode" : "", 
    "accountType" : "International", 
    "country" : "United State", 
    "organization" : "555af07389025b2b58759bca", 
    "isActive" : True, 
    "templateId" : "5649d0c9087df204a8a71636", 
    "relations" : {
        "parentAccounts" : [
            {
                "accountName" : "CHRYSLER MASTER", 
                "id" : "56a1e9773f26c121381e579d", 
                "accountNumber" : "CHRYSLER_M"
            }
        ]
    }, 
    "shipmentProfile" : "", 
    "groupName" : "Chrysler"
},
{ 
    "_id" : "5714e51c3f26c1195f9a2d62", 
    "city" : "COLUMBUS", 
    "system" : "5649d0ce087df204a8a71638", 
    "countryCode" : " US", 
    "accountNumber" : "635434", 
    "address1" : " 8809 MACON RD", 
    "address2" : "COLUMBUS", 
    "templateId" : "5649d0c9087df204a8a71636", 
    "zipCode" : " 31901", 
    "relations" : {
        "childrenAccounts" : [
        ], 
        "parentAccounts" : [
            {
                "accountNumber" : "UTC_M", 
                "id" : "56d45ecf3f26c1675d83c087", 
                "accountName" : "UTC"
            }
        ]
    }, 
    "accountName" : "PRATT & WHITNEY", 
    "state" : "Georgia", 
    "stateCode" : "GA", 
    "country" : " UNITED STATES", 
    "parentAccounts" : "UTC_M", 
    "organization" : "555af07389025b2b58759bca", 
    "id" : "null", 
    "isActive" : True, 
    "groupName" : "UTC"
}]

df = pd.read_json(account_data)
df.to_csv('output.csv')
