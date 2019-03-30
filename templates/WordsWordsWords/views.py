from flask import request
from templates import app


@app.route('/')
def index():
    return 'Hello'


@app.route('/ping', methods=['GET'])
def ping():
    if request.method == 'GET':
        return 'ping'
    return '405: Restricted method'
