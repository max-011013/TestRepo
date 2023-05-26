from bson import ObjectId
oid_str = '555fc7956cda204928c9dbab'
oid2 = ObjectId(oid_str)
print(repr(oid2))



print(type(repr(ObjectId("555af07389025b2b58759bca"))))