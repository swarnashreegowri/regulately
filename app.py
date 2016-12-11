"""The main Flask application.  To run the app: ./serve"""

from flask import Flask, Response, request, send_from_directory
import lib.mongo
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

class Encoder(json.JSONEncoder):
    def default(self, obj):
        return str(obj)

@app.route('/dockets/<id>')
def get_docket(id):
    return Response(json.dumps(lib.mongo.retrieveDocket(id), cls=Encoder),
                    mimetype='application/json')
