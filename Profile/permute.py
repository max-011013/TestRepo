_out = []



l1 = [1,2,3,4,5]

k = 120


for x in l1:
    if len(_out) == 0:
        _out.append([x])
    else:
        for j in _out:
            for k in range(len(j)+1):
                temp = []
                for l in j:
                    temp.append(l)
                temp.insert(k,i)

http://ceva-uat.invoize.com/login/

Devtestfixrepeat@123        


db.getCollection("ceva20150519134235Metadata").find({"details.chargeLine" : "1002","details.isActive" : true, "system" : ObjectId("5649d0ce087df204a8a71638")})
db.getCollection("ceva20150519134235Metadata").find({"_id" : ObjectId(""56e151f63f26c1685bcef4d5")})

db.getC


db.getCollection("ceva20150519134235Metadata").find({"details.value" : "HAWB",  "type" : "docProfile"})







def createChargeProfile(db,acc):
    chargecoll = db["chargeProfile"]
    accountColl = db["Account"]
    air = pd.read_csv("Chargeprofile.csv")
    air.to_json("_result4.json", indent =1, orient="records")
    with open("_result4.json", 'r') as jsonfile:
        info = json.loads(jsonfile.read())

    with open("airProfile.json", 'r') as jsonfile:
        deliveryData = json.loads(jsonfile.read())

    data = []
    for rec in info:
        {
        "chargeLine": rec['Charge Code'],
        "dashboardProfileBase": None,
        "chargeCodeDescription": rec['Charge Description'],
        "currencyCode": "USD",
        "templateId": "555b112889025b2b58759c57",
        "value": rec['OFS Charge Code'],
        # "updateField": false,
        "chargeText": "new charge",
        "ofsChargeCode": rec['OFS Charge Code'],
        "isActive": True,
        "chargeType": rec['Charge Type'],
        "invoiceText1": rec['Invoice Text 1'],
        "ediCode": None,
        "chargeCode": None,
        "invoiceText2": rec['Invoice Text 2'],
        # "id": "641affe4371337b393713379",
        "displayOrder": rec['Display Order']
        }
        data.append(rec)
    deliveryData["addedBy"] = "invoizeAutomation"
    deliveryData['charges'] = data


    parent = accountColl.find_one({"accountNumber":acc},{"_id":1,"accountName":1,"accountNumber":1})
    chargecoll.insert_one(deliveryData)

    delivery = chargecoll.find_one({"accountNumber":parent["accountNumber"]},{"_id":1})
    accountColl.update_one({"_id" : parent["_id"]},{
        "$push" : {
        "references.chargeProfile": delivery["_id"]
        }
    })

