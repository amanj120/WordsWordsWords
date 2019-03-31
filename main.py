#!/usr/bin/env python3
import re

from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

MONGO_URI = 'mongodb://admin:aaWyedsDgy03jcLc@cluster0-shard-00-00-kwnae.gcp.mongodb.net:27017,cluster0-shard-00-01-kwnae.gcp.mongodb.net:27017,cluster0-shard-00-02-kwnae.gcp.mongodb.net:27017/markov?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'

STARTER_SIZE = 10
WORDS_SIZE = 100
PAD_SIZE = 10

app = Flask(__name__)
CORS(app)
db = MongoClient(MONGO_URI).markov

@app.route('/')
def index():
    return 'Welcome to WordsWordsWords,\n a Shakespeare Markov Chain API'

@app.route('/words/<word>')
def words(word):
    word_regex = re.compile(re.escape(word), re.IGNORECASE)
    word_relation = db.freqs.find_one({'word': word_regex})

    if not word_relation:
        word_relation = {'word': word, 'freqs': []}

    # Extract the list of words and frequencies from this word's relations
    freq_pairs = word_relation['freqs']
    # Limit number of pairs taken
    freq_pairs = freq_pairs[:WORDS_SIZE]
    # Sort in descending order of frequency
    freq_pairs.sort(key=lambda f: -f['freq'])
    # Pad pairs with random sample
    num_left = max(0, PAD_SIZE - len(freq_pairs))
    rand_relations = db.freqs.aggregate([{'$sample': {'size': num_left}}])
    rand_words = [rand_relation['word'] for rand_relation in rand_relations]
    freq_pairs.extend([{'word': word, 'freq': 0.0} for word in rand_words])
    return jsonify(freq_pairs)

@app.route('/starters')
def starters():
    rand_words = db.starters.aggregate([{'$sample': {'size': STARTER_SIZE}}])
    rand_words = [word['word'] for word in rand_words]
    freq = 1 / len(rand_words)
    return jsonify([{'word': word, 'freq': freq} for word in rand_words])

@app.route('/<other>')
def handleIllegalRequest(other):
    return "405: Restricted method"

@app.route('/ping')
def ping():
    return 'pong'

if __name__ == '__main__':
    app.run(host='0.0.0.0')

'''
def synonyms(word):
    syn_sets = wordnet.synsets(word)
    synonyms = set()
    for syn_set in syn_sets or []:
        for lemma in syn_set.lemmas():
            synonyms.add(lemma.name())
    return synonyms
'''
