from flask import request, render_template
from templates import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ping', methods=['GET'])
def ping():
    if request.method == 'GET':
        return 'ping'
    return '405: Restricted method'
