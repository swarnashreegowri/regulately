"""
Largely derived from work by Zachary Jacobi (https://github.com/zejacobi) in the DeltaGreen project
(https://github.com/zejacobi/DeltaGreen)
"""
import unittest
import os
import mongomock
import json

from dateutil.parser import parse

import seed_db as seed_db
import constants as constants

test_data_path = os.path.join('.', 'tests', 'test_data')
test_docket = os.path.join(test_data_path, 'sample_docket.json')
test_comment = os.path.join(test_data_path, 'sample_comment.json')
json_obj = {"_id": "test"}


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.seed_db = seed_db
        self.mongo = mongomock.MongoClient()['Test']
        self.seed_db.database = self.mongo

    def test_mock(self):
        """Ensure that the database has been successfully mocked"""
        self.assertEqual(self.seed_db.database.client.address, ('localhost', 27017))

    def test_insert(self):
        """Ensure that the insert function works"""
        self.assertEqual(self.seed_db.insert({"_id": "test"}, 'test'), 'test')  # give back _id
        self.assertEqual(self.mongo['test'].find()[0], {"_id": 'test'})  # inserted the record


class TestDocketAPI(unittest.TestCase):
    """"Test the regulations.gov documents API queries"""

    def test_get_category_documents(self):
        """Valid category should provide list of documents and category should be added to JSON"""
        category = 'EELS'
        document_type = 'PR'

        fetched_json_obj = seed_db.get_category_documents(category, document_type, 10, True)
        self.assertTrue('docketId' in fetched_json_obj['documents'][0])

    def test_get_docket(self):
        """Valid docket id should return JSON record with docket-specific fields"""
        query_id = 'EPA-HQ-OAR-2014-0198'
        document = {'docketId': query_id}
        category = 'PRE'
        fetched_json_obj = seed_db.get_docket(document, category)
        self.assertTrue('docketAbstract' in fetched_json_obj)
        self.assertEqual(fetched_json_obj['docketId'], query_id)
        self.assertEqual(fetched_json_obj['category'], constants.REGULATION_CATEGORIES[category])
        self.assertEqual(fetched_json_obj['openForComment'], None)

    def test_get_invalid_docket(self):
        """Invalid docket id should return None"""
        document = 'NOT-VALID-DOCUMENT-STRING'
        category = 'PRE'
        fetched_json_obj = seed_db.get_docket(document, category)
        self.assertIsNone(fetched_json_obj)

    def test_get_docket_comments(self):
        """Valid category should provide list of documents and category should be added to JSON"""
        query_id = 'USCG-2000-7080'
        fetched_json_obj = seed_db.get_docket_comments(query_id)
        self.assertTrue('docketId' in fetched_json_obj[0])
        self.assertEqual(fetched_json_obj[0]['documentType'], 'Public Submission')

        query_id = 'EPA-HQ-OPP-2015-0560'  # had no comments as of Dec 12, 2016
        fetched_json_obj = seed_db.get_docket_comments(query_id)
        self.assertFalse(fetched_json_obj)


class TestAddDateInformation(unittest.TestCase):
    """"Test adding date information to retrieved dockets and comments from the regulations.gov API"""

    def setUp(self):
        with open(test_docket) as data_file:
            self.docket = json.load(data_file)

    def test_add_timeline_events(self):
        """Should add latestTimelineEvent and firstTimelineEvent fields that match sample_docket.json"""
        docket = seed_db.add_timeline_events(self.docket)

        self.assertEqual(docket['firstTimelineEvent'], parse('12/01/2000', dayfirst=False))
        self.assertEqual(docket['latestTimelineEvent'], parse('08/29/2016', dayfirst=False))

    def test_parse_api_date(self):
        date_strings = ["06/08/2016", "08/29/2006", "01/00/2017", "03/01/2001"]
        expected_dates = [parse(d, dayfirst=False) for d in ["06/08/2016", "08/29/2006", "01/01/2017", "03/01/2001"]]

        self.assertSequenceEqual([seed_db.parse_api_date(d) for d in date_strings], expected_dates)
