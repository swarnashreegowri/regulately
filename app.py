"""The main Flask application.  To run the app: ./serve"""

from flask import Flask, Response, request, send_from_directory
import json

app = Flask('regulately')

@app.route('/static/<path:path>')
def static_file(path):
    return send_from_directory('static', path)

@app.route('/')
def main_page():
    return '''
<link rel="stylesheet" href="static/style.css">
Welcome to Regulately!
'''

@app.route('/dockets/<id>')
def get_docket(id):
    return Response(json.dumps({
        'title': 'Docket %s' % id,
        'num_comments': 0,
        'abstract': 'A thing.',
        'sentiment': {
            'positive': 0,
            'negative': 0,
            'neutral': 0,
            'rating': 0
        },
        'comment_start_date': '2016-01-01',
        'comment_end_date': '2016-12-01',
        'is_open': True,
        'topic': [],
        'agency': 'EELS',
        'comment_summary': {
            'word_cloud': {},
        },
        'comments': [
            {
                'text': 'A comment.',
                'sentiment': 0,
                'length': 123,
            }
        ]
    }), mimetype='application/json')
