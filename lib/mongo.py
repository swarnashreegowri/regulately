from pymongo import MongoClient
from external_services import DATABASE, MONGO_STRING

client = MongoClient(MONGO_STRING + DATABASE)
database = client[DATABASE]
dockets = database['dockets']

# def insertDockets (newDockets) :
# 	dockets.insert(newDockets)

def retreiveDockets (categories = ""):
	# takes an array of categories ex: ["nature"]
	retrievedDockets = []
	if categories :
		for retreivedDocket in dockets.find({'topic': {'$in' : categories}}):
			retrievedDockets.append(retreivedDocket)
	else :
		for retreivedDocket in dockets.find():
			retrievedDockets.append(retreivedDocket)
		print(retrievedDockets)

	return retrievedDockets

def retreiveDocket (docketID):
	docket = dockets.find_one({'id': docketID})
	return Docket

