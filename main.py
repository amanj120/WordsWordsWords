import json
import random

from flask import Flask, jsonify


STARTER_SIZE = 10
RANDOM_SIZE = 10
# MONGO_URI = 'mongodb+srv://words_app:vQy9e9PUZA6ZWPMm@cluster0-kwnae.gcp.mongodb.net/markov?retryWrites=true'


app = Flask(__name__)
# app.config['MONGO_URI'] = MONGO_URI
# mongo = PyMongo(app)
# db = MongoClient(MONGO_URI).get_database()


with open('starters.json', 'r') as starters_file:
    starter_list = json.load(starters_file)
with open('freqs.json', 'r') as freqs_file:
    freqs = json.load(freqs_file)
word_list = freqs.keys()


@app.route('/')
def index():
    return 'Welcome to WordsWordsWords,\n a Shakespeare Markov Chain API'

@app.route('/words/<word>')
def words(word):
    if word != 'I':
        word = word.lower()
    freq_pairs = freqs.get(word, [])
    # Sort in descending order of frequency
    freq_pairs.sort(key=lambda f: -f['freq'])
    # Limit number of pairs taken
    freq_pairs = freq_pairs[:RANDOM_SIZE]
    # Pad pairs with random sample
    num_left = RANDOM_SIZE - len(freq_pairs)
    rand_words = random.sample(word_list, num_left)
    freq_pairs.extend([{'word': word, 'freq': 0.0} for word in rand_words])
    return jsonify(freq_pairs)

@app.route('/starters')
def starters():
    rand_words = random.sample(starter_list, STARTER_SIZE)
    return jsonify(rand_words)

@app.route('/<other>')
def handleIllegalRequest(_):
    return "405: Restricted method"

@app.route('/ping')
def ping():
    return "on database: " + 'null' # db.name


'''
def synonyms(word):
    syn_sets = wordnet.synsets(word)
    synonyms = set()
    for syn_set in syn_sets or []:
        for lemma in syn_set.lemmas():
            synonyms.add(lemma.name())
    return synonyms
'''
