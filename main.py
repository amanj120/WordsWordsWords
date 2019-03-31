import re

from flask import Flask, jsonify
from flask_pymongo import PyMongo
from nltk.corpus import wordnet


STARTER_SIZE = 10
RANDOM_SIZE = 10
MONGO_URI = 'mongodb+srv://words_app:vQy9e9PUZA6ZWPMm@cluster0-kwnae.gcp.mongodb.net/markov?retryWrites=true'


app = Flask(__name__)
app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)


def synonyms(word):
    syn_sets = wordnet.synsets(word)
    synonyms = set()
    for syn_set in syn_sets or []:
        for lemma in syn_set.lemmas():
            synonyms.add(lemma.name())
    return synonyms

@app.route('/')
def index():
    return 'Welcome to WordsWordsWords,\n a Shakespeare Markov Chain API'

@app.route('/words/<word>')
def words(word):
    word_regex = re.compile(re.escape(word), re.IGNORECASE)
    word_relation = mongo.db.freqs.find_one({'word': word_regex})

    if not word_relation:
        # Sample random documents from database
        rand_relations = mongo.db.freqs.aggregate([{'$sample': {'size': RANDOM_SIZE}}])
        # Extract the 'word' property from each of the documents
        rand_words = [rand_relation['word'] for rand_relation in rand_relations]
        freq = 1 / len(rand_words)
        return jsonify([{'word': word, 'freq': freq} for word in rand_words])

    # Extract the list of words and frequencies from this word's relations
    freq_pairs = word_relation['freqs']
    # Sort in descending order of frequency
    freq_pairs.sort(key=lambda f: -f['freq'])
    # Limit number of pairs taken
    freq_pairs = freq_pairs[:RANDOM_SIZE]
    # Pad pairs with random sample
    num_left = RANDOM_SIZE - freq_pairs
    rand_relations = mongo.db.freqs.aggregate([{'$sample': {'size': num_left}}])
    rand_words = [rand_relation['word'] for rand_relation in rand_relations]
    freq_pairs.extend([{'word': word, 'freq': 0.0} for word in rand_words])
    return jsonify(freq_pairs)

@app.route('/starters')
def starters():
    rand_words = mongo.db.starters.aggregate([{'$sample': {'size': 20}}])
    # Extract 'word' property of each of the queried documents
    rand_words = [word['word'] for word in rand_words]
    return jsonify(rand_words)

@app.route('/<other>')
def handleIllegalRequest(_):
    return "405: Restricted method"

@app.route('/ping')
def ping():
    return "on database: " + mongo.db.name
