import random

from flask import Flask, jsonify
from flask_pymongo import PyMongo


STARTER_SIZE = 20
RANDOM_SIZE = 20


app = Flask(__name__)
app.config['MONGO_URI'] = 'TODO'
mongo = PyMongo(app)

starters = [word['word'] for word in mongo.db.starters.find({})]


@app.route('/')
def landingPage():
    return 'welcome to words words words,\n a shakespeare markov chain api'

@app.route('/getwords/<word>')
def getwords(word):
    word_relation = mongo.db.freqs.find_one({'word': word})
    if not word_relation:
        rand_relations = mongo.db.freqs.aggregate({'$sample': {'size': RANDOM_SIZE}})
        return jsonify([rand_relation['word'] for rand_relation in rand_relations])
    freq_pairs = word_relation['freqs']
    freq_pairs.sort(key=lambda f: -f['freq'])
    return jsonify(freq_pair['word'] for freq_pair in freq_pairs)

@app.route('/getstarters')
def getstarters():
    words = random.sample(starters, STARTER_SIZE)
    return jsonify(words)

@app.route('/<other>')
def handleIllegalRequest(other):
    return "Error 400"

@app.route('/ping')
def ping():
    return 'ping'

if __name__ == '__main__':
    app.run()
