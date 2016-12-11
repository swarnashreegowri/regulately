from pymongo import MongoClient
from pymongo.operations import UpdateOne
from external_services import DATABASE, MONGO_STRING

client = MongoClient(MONGO_STRING + DATABASE)
database = client[DATABASE]

SEED_DATA = [
    {
        'id': '1',
        'title': 'Fake Docket',
        'num_comments': 1,
        'abstract': 'A thing.',
        'sentiment': {
            'positive': 0,
            'negative': 0,
            'neutral': 0,
            'rating': 0
        },
        'category': ["environment", "politics"],
        'comment_start_date': '2016-01-01',
        'comment_end_date': '2016-12-01',
        'is_open': True,
        'topic': [],
        'agency': 'EELS',
        'comment_summary': {
            'word_cloud': {},
        },
        'comments': [
            {
                'text': 'A comment.',
                'sentiment': 0,
                'length': 123,
            }
        ]
    },
    {
        'id': '2',
        'title': 'Fake Docket 2',
        'num_comments': 1,
        'abstract': 'Mor good info.',
        'sentiment': {
            'positive': 0,
            'negative': 0,
            'neutral': 0,
            'rating': 0
        },
        'comment_start_date': '2016-01-01',
        'comment_end_date': '2016-12-01',
        'is_open': True,
        'topic': ["law", "politics"],
        'agency': 'EELS',
        'comment_summary': {
            'word_cloud': {},
        },
        'comments': [
            {
                'text': 'A comment.',
                'sentiment': 0,
                'length': 123,
            }
        ]
    }
]

dockets = database['dockets']
comments = database['comments']

def insertDockets (newDockets) :
    dockets.insert(newDockets)

# def retrieveDockets ():
#     print (retrieveDockets)

def retrieveDocket (docketID):
    docket = dockets.find_one({'docketId': docketID})
    return docket

# insertDockets(newDockets)
#

def update_dockets(docket_items):
    dockets.bulk_write(
        [UpdateOne({'_id': item['_id']}, item) for item in docket_items])

def retrieve_comments():
    return comments.find()

def retrieve_comments_by_docket_id(docket_id):
    return comments.find({'docketId': docket_id})

def update_comments(comment_items):
    comments.bulk_write(
        [UpdateOne({'_id': item['_id']}, item) for item in comment_items])
