from pymongo import MongoClient
from pymongo.operations import UpdateOne

from lib.external_services import DATABASE, MONGO_STRING

client = MongoClient(MONGO_STRING + DATABASE)
database = client[DATABASE]

dockets = database['dockets']
comments = database['comments']

# def insertDockets (newDockets) :
#     dockets.insert(newDockets)

def retrieveDockets(count, categories=[], isOpen=False):
    # takes an array of categories ex: ["nature"]
    retrievedDockets = []
    findFilter = {}
    if categories :
        findFilter['category'] = {'$in' : categories}
    if isOpen:
        findFilter['openForComment'] = True
    for retrievedDocket in dockets.find(findFilter).sort('sortDate', -1).limit(count):
        retrievedDockets.append(retrievedDocket)
    return retrievedDockets

def retrieveDocket(docketID):
    return dockets.find_one({'docketId': docketID})

def update_dockets(field, value_map):
    dockets.bulk_write(
        [UpdateOne({'docketId': docket_id}, {'$set': {field: value}})
         for docket_id, value in value_map.items()])

def retrieve_comments(count):
    return comments.find().sort("postedDate", -1).limit(count)

def retrieve_comments_by_docket_id(docket_id, count):
    return comments.find({'docketId': docket_id}).sort("postedDate", -1).limit(count)

def update_comments(field, value_map):
    comments.bulk_write(
        [UpdateOne({'documentId': comment_id}, {'$set': {field: value}})
         for comment_id, value in value_map.items()])
