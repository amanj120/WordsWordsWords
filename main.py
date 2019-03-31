import json
import random

from flask import Flask, jsonify

STARTER_SIZE = 10
WORDS_SIZE = 100
PAD_SIZE = 10

app = Flask(__name__)

with open('starters.json', 'r') as starters_file:
    starter_list = set(json.load(starters_file))
with open('freqs.json', 'r') as freqs_file:
    freqs = json.load(freqs_file)
word_list = set(freqs.keys())

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
    freq_pairs = freq_pairs[:WORDS_SIZE]
    # Pad pairs with random sample
    num_left = max(0, PAD_SIZE - len(freq_pairs))
    rand_words = random.sample(word_list, num_left)
    freq_pairs.extend([{'word': word, 'freq': 0.0} for word in rand_words])
    return jsonify(freq_pairs)

@app.route('/starters')
def starters():
    rand_words = random.sample(starter_list, STARTER_SIZE)
    return jsonify(rand_words)

@app.route('/<other>')
def handleIllegalRequest(other):
    return "405: Restricted method"

@app.route('/ping')
def ping():
    return 'ping'

'''
def synonyms(word):
    syn_sets = wordnet.synsets(word)
    synonyms = set()
    for syn_set in syn_sets or []:
        for lemma in syn_set.lemmas():
            synonyms.add(lemma.name())
    return synonyms
'''
