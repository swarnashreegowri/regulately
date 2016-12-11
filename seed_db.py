"""
Script to get 10 Final Rules and Pending Rules for a particular category on regulations.gov and upload the rules and
associated comments to MongoDB.

MongoDB communication derived from work by Zachary Jacobi (https://github.com/zejacobi) in the DeltaGreen project
(https://github.com/zejacobi/DeltaGreen)
"""

import requests
import logging
import re

from dateutil.parser import parse

from lib.mongo import database
from lib.external_services import REG_API_KEY

import constants

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def insert(json_doc, collection):
    """
    Function for inserting JSON files into a database

    :param dict json_doc: A valid python dictionary, which will be converted to JSON as it is
        inserted.
    :param str collection: The collection to insert the document into
    :return: The unique ID given to the inserted item
    """
    return database[collection].insert(json_doc)


def get_category_documents(category, document_type, results_per_page, comments_open):
    """
    Get a list of documents in a particular category

    Explanation of additional parameters used in API query:
        - cp: comment period. Set to O (Open)
        - cs: comment period closing soon. Set to 90 (days until closing)

    :param str category: Category of docket. One of the keys to REGULATION_CATEGORIES stored in constants.py
    :param str document_type: One of N: Notice, PR: Proposed Rule, FR: Rule, O: Other, SR: Supporting & Related Material
        PS: Public Submission
    :param results_per_page: Number of records to return per query (since we're not doing a paged query). Max 1000.
    :return: A JSON object containing 'documents', a list of document records returned by the API and an added
        'category' field.
    """
    search_parameters = {'api_key': REG_API_KEY,
                         'cat': category,
                         'dct': document_type,
                         'rpp': results_per_page,
                         'cp': 'O',
                         'cs': 90}
    fetched_docket = requests.get('https://api.data.gov/regulations/v3/documents', params=search_parameters)
    return fetched_docket.json()


def get_docket(document, category,):
    """
    Fetch a specific docket by id

    :param str document: A JSON object containing a document records returned by the regulations.gov API
    :param str category: Category of docket. One of the keys to REGULATION_CATEGORIES stored in constants.py
    :return: A string containing the JSON returned by the regulations.gov API. None if received a 'status' field (which
        indicates some kind of error)
    """
    if 'docketId' not in document:
        return None

    search_parameters = {'api_key': REG_API_KEY, 'docketId': document['docketId']}
    fetched_docket = requests.get('https://api.data.gov/regulations/v3/docket', params=search_parameters)

    if fetched_docket.status_code != 200:
        return None

    # Add category field and whether open for comment
    docket_obj = fetched_docket.json()
    docket_obj['categoryId'] = category
    docket_obj['category'] = constants.REGULATION_CATEGORIES[category]
    docket_obj['openForComment'] = document.get('openForComment')

    # Define date information for sorting
    docket_obj = add_sort_date(docket_obj, document.get('commentDueDate'))

    return docket_obj


def get_docket_comments(docket_id):
    """
    Get a list of public submissions (AKA comments) on a particular docket

    Explanation of additional parameters used in API query:
        - dct: document type. Set to PS (public submission)
        - rpp: results per page. Set to maximum allowed value

    :param str docket_id: A valid ID of a docket in regulations.gov, e.g. 'EPA-HQ-OAR-2014-0198'
    :return: A JSON object containing a list of document records returned by the regulations.gov API
    """
    search_parameters = {'api_key': REG_API_KEY, 'dktid': docket_id, 'dct': 'PS', 'rpp': 1000}
    fetched_comments = requests.get('https://api.data.gov/regulations/v3/documents', params=search_parameters)

    if fetched_comments.status_code != 200:
        return None

    comments_obj = fetched_comments.json()
    return comments_obj['documents'] if 'documents' in comments_obj else None


def add_sort_date(docket_obj, comment_due_date):
    """

    :param dict docket_obj: A JSON object containing a docket record returned by the regulations.gov API.
    :param str comment_due_date: String containing comment due date. May be None.
    :return: A JSON object containing docket_obj with added field 'sortDate' and (possibly) fields:
        'latestTimelineEvent', 'firstTimelineEvent', 'commentDueDate'
    """

    docket_obj = add_timeline_events(docket_obj)
    docket_obj['sortDate'] = docket_obj.get('latestTimelineEvent')

    if comment_due_date:
        docket_obj['commentDueDate'] = parse_api_date(comment_due_date)
        docket_obj['sortDate'] = comment_due_date  # overwrite previous value

    return docket_obj


def add_timeline_events(docket_obj):
    """
    Add two fields, 'latestTimelineEvent' and 'firstTimelineEvent', to the docket. Dockets have a large number of
        possible events associated with them (e.g. opening for preliminary comments, final ruling), so this is intended
        to allow us to sort dockets by timeline.

    :param dict docket_obj: A JSON object containing a docket record returned by the regulations.gov API.
    :return: A JSON object containing docket_obj and (possibly) fields 'latestTimelineEvent' and 'firstTimelineEvent'
    """

    if 'timeTables' not in docket_obj:
        return docket_obj

    # Get all timeline dates
    date_strings = [d.get('date') for d in docket_obj['timeTables'] if d.get('date')]
    dates = [parse_api_date(d) for d in date_strings]

    docket_obj['latestTimelineEvent'] = max(dates) if dates else None
    docket_obj['firstTimelineEvent'] = min(dates) if dates else None

    return docket_obj


def parse_api_date(date_string):
    """
    Parse dates from API. Cannot simply use dateutil because occasionally the month/day is set to '00'. Assumes that
        substituting '01' is an acceptable alternative.
    :param str date_string: Date strings. Expected to be parseable except for occasionally containing dates of the
        form 'dd/mm/yyyy' where 'mm' = '00'
    :return: List of parsed date objects.
    """
    return parse(re.sub(r'/00/', r'/01/', date_string), dayfirst=False)


if __name__ == '__main__':
    documents = []
    for document_type in 'PR', 'FR':
        documents.extend(get_category_documents(category=constants.QUERY_CATEGORY,
                                                document_type=document_type,
                                                results_per_page=constants.RESULTS_PER_QUERY//2,
                                                comments_open=constants.QUERY_IS_OPEN)['documents'])

    for document in documents:
        # Fetch from API- will be None if there was an error
        docket = get_docket(document, constants.QUERY_CATEGORY)

        if not docket:
            continue

        # Insert docket and comments into database
        insert(docket, 'dockets-dated')
        comments = get_docket_comments(docket['docketId'])

        if comments:
            insert(comments, 'comments-dated')

        logging.info('Completed docket upload for id: {}'.format(docket['docketId']))
