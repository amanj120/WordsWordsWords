import re
import sys

from flask import Flask, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
from nltk.corpus import wordnet


STARTER_SIZE = 20
RANDOM_SIZE = 20


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://words_app:vQy9e9PUZA6ZWPMm@cluster0-kwnae.gcp.mongodb.net/markov?retryWrites=true'
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
        rand_relations = mongo.db.freqs.aggregate([{'$sample': {'size': RANDOM_SIZE}}])
        return jsonify([rand_relation['word'] for rand_relation in rand_relations])
    freq_pairs = word_relation['freqs']
    freq_pairs.sort(key=lambda f: -f['freq'])
    return jsonify([freq_pair['word'] for freq_pair in freq_pairs])

@app.route('/starters')
def starters():
    rand_words = mongo.db.starters.aggregate([{'$sample': {'size': 20}}])
    print([w for w in rand_words])
    for word in rand_words:
        print(word)
    return jsonify([word['word'] for word in rand_words])

@app.route('/<other>')
def handleIllegalRequest(_):
    return "405: Restricted method"

@app.route('/ping')
def ping():
    return mongo.db.name


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--update-db':
        from shakespeare_model import update_db
        admin_client = MongoClient('mongodb+srv://admin:aaWyedsDgy03jcLc@cluster0-kwnae.gcp.mongodb.net/markov?retryWrites=true')
        update_db(admin_client.get_database())
    else:
        app.run()
