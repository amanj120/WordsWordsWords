from flask import Blueprint, jsonify, request
from flask import Flask
from flask_cors import CORS
import pymongo


app = Flask(__name__)

CORS(app)

if __name__ == '__main__':
    app.run()

@app.route("/ping", methods=['GET'])
def ping():
    if request.method == 'GET':
        return "ping"
    else:
        return "405: Restricted method"

