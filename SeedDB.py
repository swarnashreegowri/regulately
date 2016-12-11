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
from Queue import Queue

from Lib.Mongo import database
from ExternalServices import REG_API_KEY
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


def get_category_documents(category, document_type, rules_per_page):
    """

    :param category: Category of docket.
    :param document_type: One of N: Notice, PR: Proposed Rule, FR: Rule, O: Other, SR: Supporting & Related Material,
        PS: Public Submission
    :param rules_per_page: Number of records to return.
    :return: List of dockets by category
    """
    search_parameters = {'api_key': REG_API_KEY, 'cat': category, 'dct': document_type, 'rpp': rules_per_page}
    fetched_docket = requests.get('https://api.data.gov/regulations/v3/documents', params=search_parameters)
    return fetched_docket.json()


def get_docket(docket_id):
    """

    :param str docket_id: A valid ID of a docket in regulations.gov, e.g. 'EPA-HQ-OAR-2014-0198'
    :return: A string containing the JSON
    """
    search_parameters = {'api_key': REG_API_KEY, 'docketId': docket_id}
    fetched_docket = requests.get('https://api.data.gov/regulations/v3/docket', params=search_parameters)
    return fetched_docket.json()


def get_docket_comments(docket_id):
    """

    :param str docket_id: A valid ID of a docket in regulations.gov, e.g. 'EPA-HQ-OAR-2014-0198'
    :return:
    """
    search_parameters = {'api_key': REG_API_KEY, 'dktid': docket_id, 'dct': 'PS', 'rpp': 1000}
    fetched_docket = requests.get('https://api.data.gov/regulations/v3/documents', params=search_parameters)
    return fetched_docket.json()


def worker():
    """
    Worker thread
    """
    # TODO: worker thread inserts docket + comments into mongoDB
    # while True:
    #     item = q.get()
    #     if item is None:
    #         break
    #
    #     json_obj, collection_name = parse_json(item)
    #     insert(json_obj, collection_name)
    #     q.task_done()

if __name__ == '__main__':
    try:
        directory = sys.argv[1]
    except IndexError:
        print('Error: No directory supplied.')
        exit()

    json_dir = os.path.join(os.curdir, directory)

    # TODO: get 10 PR and 10 FR dockets for each category, join with 100 associated comments, push to MongoDB
    #
    # # Add
    #
    # for i in range(num_threads):
    #     t = Thread(target=worker, daemon=True)
    #     t.start()
    #     threads.append(t)
    #
    # for rule in rules:
    #     docket_id = rule['docketId']
    #     docket = get_docket(docket_id)
    #
    #     # Add docket ID to queue
    #     q.put(docket)
    #
    # q.join()
    #
    # for i in range(num_threads):
    #     q.put(None)
    # for t in threads:
    #     t.join()
