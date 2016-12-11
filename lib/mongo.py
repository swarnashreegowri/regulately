from pymongo import MongoClient
from pymongo.operations import UpdateOne
from external_services import DATABASE, MONGO_STRING

client = MongoClient(MONGO_STRING + DATABASE)
database = client[DATABASE]

dockets = database['dockets']
comments = database['comments']

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
			
	return retrievedDockets

def retreiveDocket (docketID):
	docket = dockets.find_one({'id': docketID})
	return Docket

def update_dockets(field, value_map):
    dockets.bulk_write(
        [UpdateOne({'docketId': docket_id}, {'$set': {field: value}})
         for docket_id, value in value_map.items()])

def retrieve_comments():
    return comments.find()

def retrieve_comments_by_docket_id(docket_id):
    return comments.find({'docketId': docket_id})

def update_comments(field, value_map):
    comments.bulk_write(
        [UpdateOne({'documentId': comment_id}, {'$set': {field: value}})
         for comment_id, value in value_map.items()])
