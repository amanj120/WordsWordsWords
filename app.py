from flask import request
from flask import Flask
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config['MONGO_URI'] = 'TODO'
mongo = PyMongo(app)


if __name__ == '__main__':
    app.run()


@app.route('/ping', methods=['GET'])
def ping():
    if request.method == 'GET':
        return 'ping'
    return '405: Restricted method'
