from flask import request
from flask import Flask
from flask_pymongo import PyMongo
from flask import jsonify


app = Flask(__name__)
app.config.from_object('configurations.DevelopmentConfig')
mongo = PyMongo(app)


@app.route('/')
def landingPage():
    return 'welcome to words words words,\n a shakespeare markov chain api'

@app.route('/getwords/<first>/<second>')
def getwords(first, second):
    return jsonify(backendGetWords(first,second))

@app.route('/getstart')
def getstart():
    return jsonify(backendGetStart())

def backendGetWords(first, second):
    ret = []
    ret.append(first)
    ret.append(second)
    return ret

def backendGetStart():
    ret = ["hello", "my", "name"]
    return ret;

@app.route('/<other>')
def handleIllegalRequest(other):
    return "Error: Illegal Request"

@app.route('/ping')
def ping():
    return 'ping'

if __name__ == '__main__':
    app.run()
