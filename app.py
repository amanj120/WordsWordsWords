from flask import request
from flask import Flask
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config.from_object('configurations.DevelopmentConfig')
mongo = PyMongo(app)


@app.route('/')
def hello():
    return 'Hello'


@app.route('/ping', methods=['GET'])
def ping():
    if request.method == 'GET':
        return 'ping'
    return '405: Restricted method'


if __name__ == '__main__':
    app.run()
