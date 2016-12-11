import datetime
import dateutil.parser
from pymongo import MongoClient
from pymongo.operations import UpdateOne

from lib.external_services import DATABASE, MONGO_STRING

client = MongoClient(MONGO_STRING + DATABASE)
database = client[DATABASE]

dockets = database['dockets']
comments = database['comments']
categories = database['categories']

# def insertDockets (newDockets) :
#     dockets.insert(newDockets)

def retrieveDockets(count, categories, isOpen, daysLeftToComment):
    # takes an array of categories ex: ["nature"]
    retrievedDockets = []
    today = datetime.datetime.now()
    findFilter = {}
    if categories :
        findFilter['category'] = {'$in' : categories}
    if isOpen:
        findFilter['openForComment'] = True
    if daysLeftToComment:
        dO = datetime.datetime(today.year, today.month, today.day)
        end_date = datetime.datetime.now() + datetime.timedelta(days=daysLeftToComment)
        dT = datetime.datetime(end_date.year, end_date.month, end_date.day)
        findFilter["commentDueDate"] = {'$gt' : dO, '$lt': dT}

    for retrievedDocket in dockets.find(findFilter).sort('sortDate', -1).limit(count):
        retrievedDockets.append(retrievedDocket)
    return retrievedDockets

def retrieveDocket(docketID):
    return dockets.find_one({'docketId': docketID})

def update_dockets(field, value_map):
    dockets.bulk_write(
        [UpdateOne({'docketId': docket_id}, {'$set': {field: value}})
         for docket_id, value in value_map.items()])

def retrieve_comments(count=1000):
    return comments.find().sort("postedDate", -1).limit(count)

def retrieve_comments_by_docket_id(docket_id, count):
    return comments.find({'docketId': docket_id}).sort("postedDate", -1).limit(count)

def update_comments(field, value_map):
    comments.bulk_write(
        [UpdateOne({'documentId': comment_id}, {'$set': {field: value}})
         for comment_id, value in value_map.items()])

def retrieve_categories():
    return categories.find()

def rewrite_categories(category_items):
    categories.delete_many({})
    categories.insert_many(category_items)
