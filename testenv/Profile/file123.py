from pymongo import MongoClient
import pandas as pd
import json


class upadte_new_JSON:
    def create_connection(self):
        #create a connection with valid userId and password
        client = MongoClient('mongodb://localhost:27017')
        db = client["bhaskarad_db"]
        print("connected successfuly")
        return db
    # Insert Data into database from Excel
    def sheetData(self,db):
        chargeProfile = {}
        charges = []
        df = pd.read_excel('Automation.xlsx',engine='openpyxl',sheet_name='Charge Profile')
        data = df.to_json(orient='records')
        data2=json.loads(data)
        collection_inf = db["sample"]
        
        for item in data2:
            sample_data = {}
            if item['Charge Code']:
                sample_data['chargeLine'] = item['Charge Code']
            else:
                sample_data['chargeLine'] = ""

            sample_data['rateTariff'] = None
            sample_data['chargeText'] = ""
            sample_data['id'] = ''
            if item['Display Order']:
                sample_data['displayOrder'] = item['Display Order']
            else:
                sample_data['displayOrder'] = ""

            sample_data['rateID'] = None
            if item['Display Order']:
                sample_data['currencyCode'] = item['Default Currency']
            else:
                sample_data['currencyCode'] = ""

            sample_data['system'] = "5649d0ce087df204a8a71638"

            if item['OFS Charge Code']:
                sample_data['ofsChargeCode'] = item['OFS Charge Code']
            else:
                sample_data['ofsChargeCode'] = ""

            sample_data['select'] = True
            sample_data['chargeCode'] = ""

            if item['Charge Description']:
                sample_data['chargeCodeDescription'] = item['Charge Description']
            else :
                sample_data['chargeCodeDescription'] = ""
            if item['Charge Type']:
                sample_data['chargeType'] = item['Charge Type']
            else:
                sample_data['chargeType'] = ""

            sample_data['turnoverGroup'] = None
            sample_data['chargeLevel'] = None
            sample_data['isActive'] = True
            sample_data['racp'] = None
            sample_data['country'] = None
            sample_data['value'] = ""
            sample_data['serviceCode'] = None
            sample_data['templateId'] = "555b112889025b2b58759c57"
            sample_data['ediCode'] = None
            if item['Invoice Text 1']:
                sample_data['invoiceText1'] = item['Invoice Text 1']
            else :
                 sample_data['invoiceText1'] = ""
            if item['Invoice Test 2']:
                sample_data['invoiceText2'] = item['Invoice Test 2']
            else:
                sample_data['invoiceText2'] = ""
            sample_data['paymentTerm'] = None
            
            charges.append(sample_data)

        chargeProfile["charges"] = charges
        chargeProfile["addedBy"] = "invoizeAutomation"
        chargeProfile["systemId"] = "5649d0ce087df204a8a71638"
        chargeProfile["templateId"] = "555b112889025b2b58759c57"
        chargeProfile["profileName"] = acc
        chargeProfile["accountId"] = str(parent["_id"])
        update_data = collection_inf.insert_one(chargeProfile)

        if update_data:
            print("Added Successfully")
        return 0
            
obj=upadte_new_JSON()
db=obj.create_connection()
obj.sheetData(db)