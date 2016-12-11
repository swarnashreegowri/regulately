import app
import json

class Client:
    """A client for making test requests to our server."""
    def __init__(self):
        self.client = app.app.test_client()

    def get(self, _path, _expected_status=200, _headers={}, **kwargs):
        result = self.client.get(
            _path, headers=_headers, query_string=kwargs or None)
        assert result.status_code == _expected_status, \
            'Expected %d, got status %d: %r' % (
                _expected_status, result.status_code, result.data)
        return result

    def get_json(self, _path, _expected_status=200, _headers={}, **kwargs):
        result = self.get(_path, _expected_status, _headers, **kwargs)
        assert result.headers['Access-Control-Allow-Origin'] == '*'
        return json.loads(result.data.decode('utf-8'))
