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

@app.route('/dockets')
def get_dockets():
    count = min(int(request.args.get('count', '10')), 100)
    category = request.args.get('category', '')
    dockets = lib.mongo.retrieveDockets(count=count, categories=[category])
    return Response(json.dumps(dockets, cls=Encoder),
                    mimetype='application/json')

@app.route('/dockets/<docket_id>')
def get_docket(docket_id):
    docket = lib.mongo.retrieveDocket(docket_id)
    return Response(json.dumps(docket, cls=Encoder),
                    mimetype='application/json')

@app.route('/dockets/<docket_id>/comments')
def get_comments(docket_id):
    comments = lib.mongo.retrieve_comments_by_docket_id(docket_id)
    return Response(json.dumps(list(comments), cls=Encoder),
                    mimetype='application/json')
