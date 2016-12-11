import app
import json

client = app.app.test_client()

def test_static_file():
    r = client.get('/static/style.css')
    assert r.status_code == 200

def test_get_docket():
    r = client.get('/dockets/123')
    assert r.status_code == 200
    data = json.loads(r.data.decode('utf-8'))
    assert 'title' in data
