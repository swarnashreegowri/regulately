import app
import json

def test_static_file(client):
    client.get('/static/style.css')

def test_get_docket(client):
    data = client.get_json('/dockets/1')
    assert 'Fake Docket' in data['title']
