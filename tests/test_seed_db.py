"""
Largely derived from work by Zachary Jacobi (https://github.com/zejacobi) in the DeltaGreen project
(https://github.com/zejacobi/DeltaGreen)
"""
import unittest
import os
import mongomock
import json

import seed_db as seed_db

from constants import REGULATION_CATEGORIES

test_file = os.path.join('.', 'tests', 'test_data', 'test.json')
json_obj = {"_id": "test"}

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """generate the JSON file"""
        with open(test_file, 'w+') as file_obj:
            file_obj.write(json.dumps(json_obj))

    @classmethod
    def tearDownClass(cls):
        """remove the JSON file"""
        os.remove(test_file)

    def setUp(self):
        self.SeedDB = seed_db
        self.mongo = mongomock.MongoClient()['Test']
        self.SeedDB.database = self.mongo

    def test_mock(self):
        """Ensure that the database has been successfully mocked"""
        self.assertEqual(self.SeedDB.database.client.address, ('localhost', 27017))

    def test_insert(self):
        """Ensure that the insert function works"""
        self.assertEqual(self.SeedDB.insert({"_id": "test"}, 'test'), 'test')  # give back _id
        self.assertEqual(self.mongo['test'].find()[0], {"_id": 'test'})  # inserted the record

class TestDocketAPI(unittest.TestCase):
    """"Test the regulations.gov documents API queries"""

    @classmethod
    def setUpClass(cls):
        """generate the JSON file"""

    @classmethod
    def tearDownClass(cls):
        """remove the JSON file"""

    def test_get_category_documents(self):
        """Valid category should provide list of documents and category should be added to JSON"""
        category = 'EELS'
        document_type = 'PR'

        fetched_json_obj = seed_db.get_category_documents(category, document_type, 10)
        self.assertTrue('docketId' in fetched_json_obj['documents'][0])

    def test_get_docket(self):
        """Valid docket id should return JSON record with docket-specific fields"""
        query_id = 'EPA-HQ-OAR-2014-0198'
        category = 'PRE'
        fetched_json_obj = seed_db.get_docket(query_id, category)
        self.assertTrue('docketAbstract' in fetched_json_obj)
        self.assertEqual(fetched_json_obj['docketId'], query_id)
        self.assertEqual(fetched_json_obj['category'], REGULATION_CATEGORIES[category])

    def test_get_invalid_docket(self):
        """Invalid docket id should return JSON record with 404 Error"""
        query_id = 'NOT-VALID-ID-STRING'
        category = 'PRE'
        fetched_json_obj = seed_db.get_docket(query_id, category)
        self.assertEqual(fetched_json_obj, None)

    def test_get_docket_comments(self):
        """Valid category should provide list of documents and category should be added to JSON"""
        query_id = 'EPA-HQ-OAR-2014-0198'
        fetched_json_obj = seed_db.get_docket_comments(query_id)
        self.assertTrue('docketId' in fetched_json_obj[0])
        self.assertEqual(fetched_json_obj[0]['documentType'], 'Public Submission')

        query_id = 'EPA-HQ-OPP-2015-0560'  # had no comments as of Dec 12, 2016
        fetched_json_obj = seed_db.get_docket_comments(query_id)
        self.assertFalse(fetched_json_obj)
