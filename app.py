"""The main Flask application.  To run the app: ./serve"""

from flask import Flask, Response, request, send_file, send_from_directory
import lib.mongo
import json

app = Flask('regulately')

@app.route('/static/<path:path>')
def static_file(path):
    return send_from_directory('static', path)

@app.route('/')
def main_page():
    return send_file('index.html')

@app.route('/dockets')
def get_dockets():
    count = min(int(request.args.get('count', '10')), 100)
    category = request.args.get('category', '')
    categories = category.split(',') if category else []
    dockets = lib.mongo.retrieveDockets(count=count, categories=categories)
    return make_json_response(dockets)

@app.route('/dockets/<docket_id>')
def get_docket(docket_id):
    docket = lib.mongo.retrieveDocket(docket_id)
    return make_json_response(docket)

@app.route('/dockets/<docket_id>/comments')
def get_comments(docket_id):
    comments = lib.mongo.retrieve_comments_by_docket_id(docket_id)
    return make_json_response(list(comments))

def make_json_response(data):
    class Encoder(json.JSONEncoder):
        def default(self, obj):
            return str(obj)

    return Response(json.dumps(data, cls=Encoder),
                    mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*'})
