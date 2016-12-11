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
from external_services import REG_API_KEY
from constants import REGULATION_CATEGORIES

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Parameters for database seeding
regulation_category = 'ITT'  # enter regulation category of interest here
results_per_category = 10  # will fetch this #/2 'PR' and 'FR' records from the regulation category above


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


def get_docket(docket_id, category, comment_due_date):
    """
    Fetch a specific docket by id

    :param str docket_id: A valid ID of a docket in regulations.gov, e.g. 'EPA-HQ-OAR-2014-0198'
    :param str category: Category of docket. One of the keys to REGULATION_CATEGORIES stored in constants.py
    :param srt comment_due_date: Due date for comments on docket. Should be parseable date string.
    :return: A string containing the JSON returned by the regulations.gov API. None if received a 'status' field (which
        indicates some kind of error)
    """
    search_parameters = {'api_key': REG_API_KEY, 'docketId': docket_id}
    fetched_docket = requests.get('https://api.data.gov/regulations/v3/docket', params=search_parameters)

    if fetched_docket.status_code != 200:
        return None

    # Add category field, comment due date, and queryable date information
    docket_obj = fetched_docket.json()
    docket_obj['categoryId'] = category
    docket_obj['category'] = REGULATION_CATEGORIES[category]
    docket_obj['commentDueDate'] = parse(comment_due_date) if comment_due_date is not None else None
    docket_obj = add_timeline_events(docket_obj)

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


def add_timeline_events(docket_obj):
    """
    Add two fields, 'latestTimelineEvent' and 'firstTimelineEvent', to the docket. Dockets have a large number of
        possible events associated with them (e.g. opening for preliminary comments, final ruling), so this is intended
        to allow us to sort dockets by timeline.

    :param dict docket_obj: A JSON object containing a docket record returned by the regulations.gov API.
    :return: A JSON object containing docket_obj and two new fields: 'latestTimelineEvent' and 'firstTimelineEvent'
    """

    if 'timeTables' not in docket_obj:
        return docket_obj

    # Get all timeline dates
    date_strings = [d.get('date') for d in docket_obj['timeTables'] if d.get('date')]
    dates = parse_dates(date_strings)

    docket_obj['latestTimelineEvent'] = max(dates)
    docket_obj['firstTimelineEvent'] = min(dates)

    return docket_obj


def parse_dates(date_strings):
    """
    Parse dates from API. Cannot simply use dateutil because cccasionally the month/day is set to '00'. Assumes that
        substituting '01' is an acceptable alternative.
    :param date_strings: List of date strings. Expected to be parseable except for occasionally containing dates of the
        form 'dd/mm/yyyy' where 'mm' = '00'
    :return: List of parsed date objects with
    """
    dates = [parse(re.sub(r'/00/', r'/01/', d), dayfirst=False) for d in date_strings]
    return dates


if __name__ == '__main__':
    documents = get_category_documents(regulation_category, 'PR', results_per_category//2)['documents']
    documents.append(get_category_documents(regulation_category, 'FR', results_per_category//2)['documents'])

    for document in documents:
        if 'docketId' in document:
            docket_id = document['docketId']
            comment_due_date = document.get('commentDueDate')

            # Fetch from API- will be None if there was an error
            docket = get_docket(docket_id, regulation_category, comment_due_date)
            comments = get_docket_comments(docket_id)

            # Insert into database
            if docket:
                insert(docket, 'dockets-dated')

            if comments:
                insert(comments, 'comments-dated')

            logging.info('Completed docket upload for id: {}'.format(docket_id))
