"""
Script to get all of the JSON files into the Mongo Database

Largely derived from work by Zachary Jacobi (https://github.com/zejacobi) in the DeltaGreen project
(https://github.com/zejacobi/DeltaGreen)
"""

import json
import sys
import os
import requests

from threading import Thread
from queue import Queue

from lib.mongo import database
from external_services import REG_API_KEY
from constants import REGULATION_CATEGORIES

q = Queue()
num_threads = 2
threads = []


def insert(json_doc, collection):
    """
    Function for inserting JSON files into a database

    :param dict json_doc: A valid python dictionary, which will be converted to JSON as it is
        inserted.
    :param str collection: The collection to insert the document into
    :return: The unique ID given to the inserted item
    """
    return database[collection].insert(json_doc)


def get_category_documents(category, document_type, results_per_page):
    """
    Get a list of documents in a particular category.

    Explanation of additional parameters used in API query:
        - cp: comment period. Set to O (Open).
        - cs: comment period closing soon. Set to 90 (days until closing).

    :param str category: Category of docket. One of the keys to REGULATION_CATEGORIES stored in constants.py
    :param str document_type: One of N: Notice, PR: Proposed Rule, FR: Rule, O: Other, SR: Supporting & Related Material,
        PS: Public Submission
    :param results_per_page: Number of records to return per query (since we're not doing a paged query). Max 1000.
    :return: A JSON object containing 'documents', a list of document records returned by the API and an added
        'category' field.
    """
    search_parameters = {'api_key': REG_API_KEY, 'cat': category, 'dct': document_type, 'rpp': results_per_page}
    fetched_docket = requests.get('https://api.data.gov/regulations/v3/documents', params=search_parameters)
    return fetched_docket.json()


def get_docket(docket_id, category):
    """
    Fetch a specific docket by id.

    :param str docket_id: A valid ID of a docket in regulations.gov, e.g. 'EPA-HQ-OAR-2014-0198'
    :param str category: Category of docket. One of the keys to REGULATION_CATEGORIES stored in constants.py
    :return: A string containing the JSON returned by the regulations.gov API.
    """
    search_parameters = {'api_key': REG_API_KEY, 'docketId': docket_id}
    fetched_docket = requests.get('https://api.data.gov/regulations/v3/docket', params=search_parameters)

    docket_obj = fetched_docket.json()
    docket_obj['category'] = REGULATION_CATEGORIES[category]
    return docket_obj


def get_docket_comments(docket_id):
    """
    Get a list of public submissions (AKA comments) on a particular docket.

    Explanation of additional parameters used in API query:
        - dct: document type. Set to PS (public submission).
        - rpp: results per page. Set to maximum allowed value.

    :param str docket_id: A valid ID of a docket in regulations.gov, e.g. 'EPA-HQ-OAR-2014-0198'
    :return: A JSON object containing 'comments', a list of document records returned by the API.
    """
    search_parameters = {'api_key': REG_API_KEY, 'dktid': docket_id, 'dct': 'PS', 'rpp': 1000}
    fetched_comments = requests.get('https://api.data.gov/regulations/v3/documents', params=search_parameters)
    comments_obj = fetched_comments.json()
    return comments_obj['documents'] if 'documents' in comments_obj else []

def worker():
    """
    Worker thread
    """
    while True:
        json_obj = q.get()
        if not json_obj:
            break

        collection = 'dockets' if 'numberOfComments' in json_obj else 'comments'
        insert(json_obj, collection)
        q.task_done()

if __name__ == '__main__':
    regulation_category = 'HCFP'
    documents = get_category_documents(regulation_category, 'PR', 10)['documents']

    for i in range(num_threads):
        t = Thread(target=worker, daemon=True)
        t.start()
        threads.append(t)

    for document in documents:
        docket_id = document['docketId']
        docket = get_docket(docket_id, regulation_category)
        comments = get_docket_comments(docket_id)

        # Add docket to queue
        q.put(docket)

        # Add comments to queue
        q.put(comments)

    q.join()

    for i in range(num_threads):
        q.put(None)
    for t in threads:
        t.join()
