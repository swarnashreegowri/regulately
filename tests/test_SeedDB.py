"""
Largely derived from work by Zachary Jacobi (https://github.com/zejacobi) in the DeltaGreen project
(https://github.com/zejacobi/DeltaGreen)
"""
import unittest
import os
import mongomock
import json

import SeedDB as SeedDB

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
        self.SeedDB = SeedDB
        self.mongo = mongomock.MongoClient()['Test']
        self.SeedDB.database = self.mongo

    def test_mock(self):
        """Ensure that the database has been successfully mocked"""
        self.assertEqual(self.SeedDB.database.client.address, ('localhost', 27017))

    def test_insert(self):
        """Ensure that the insert function works"""
        self.assertEqual(self.SeedDB.insert({"_id": "test"}, 'test'), 'test')  # give back _id
        self.assertEqual(self.mongo['test'].find()[0], {"_id": 'test'})  # inserted the record

    # def test_worker(self):
    #     """Ensure that the worker function can insert JSON into the database"""
    #     self.SeedDB.q.put(test_file)
    #     t = Thread(target=self.SeedDB.worker)
    #     t.start()
    #     self.SeedDB.q.join()
    #     self.SeedDB.q.put(None)
    #     t.join()
    #     self.assertEqual(self.mongo['test'].find()[0], {"_id": 'test'})  # inserted the record

class TestDocketAPI(unittest.TestCase):
    """"Test the regulations.gov documents API queries"""

    @classmethod
    def setUpClass(cls):
        """generate the JSON file"""

    @classmethod
    def tearDownClass(cls):
        """remove the JSON file"""

    def test_get_category_documents(self):
        """"""
        category = 'EELS'
        document_type = 'PR'

        fetched_json_obj = SeedDB.get_category_documents(category, document_type, 10)
        self.assertTrue('docketId' in fetched_json_obj['documents'][0])

    def test_get_docket(self):
        """Valid docket id should return JSON record with docket-specific fields"""
        query_id = 'EPA-HQ-OAR-2014-0198'
        fetched_json_obj = SeedDB.get_docket(query_id)
        self.assertTrue('docketAbstract' in fetched_json_obj)
        self.assertEqual(fetched_json_obj['docketId'], query_id)

    def test_fetch_invalid_docket(self):
        """Invalid docket id should return JSON record with 404 Error"""
        query_id = 'NOT-VALID-ID-STRING'
        fetched_json_obj = SeedDB.get_docket(query_id)
        self.assertTrue('code' in fetched_json_obj)
        self.assertEqual(fetched_json_obj['code'], 404)
