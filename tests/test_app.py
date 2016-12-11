import app
import json
from unittest import mock

def test_static_file(client):
    client.get('/static/style.css')

def test_get_docket(client):
    with mock.patch('lib.mongo.retrieveDocket', return_value={'title': 'Foo'}):
        data = client.get_json('/dockets/1')
        assert 'Foo' in data['title']

def test_get_comments(client):
    with mock.patch('lib.mongo.retrieve_comments_by_docket_id',
                    return_value=[{'text': 'asdf'}, {'text': 'hjkl'}]):
        data = client.get_json('/dockets/1/comments')
        assert data == [{'text': 'asdf'}, {'text': 'hjkl'}]
