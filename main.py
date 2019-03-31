import re

from flask import Flask, jsonify
#from nltk.corpus import wordnet


STARTER_SIZE = 20
RANDOM_SIZE = 20
# MONGO_URI = 'mongodb+srv://words_app:vQy9e9PUZA6ZWPMm@cluster0-kwnae.gcp.mongodb.net/markov?retryWrites=true'
MONGO_URI = 'mongodb://admin:aaWyedsDgy03jcLc@cluster0-shard-00-00-kwnae.gcp.mongodb.net:27017,cluster0-shard-00-01-kwnae.gcp.mongodb.net:27017,cluster0-shard-00-02-kwnae.gcp.mongodb.net:27017/?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'


app = Flask(__name__)
# app.config['MONGO_URI'] = MONGO_URI
# mongo = PyMongo(app)
db = MongoClient(MONGO_URI).markov

'''
def synonyms(word):
    syn_sets = wordnet.synsets(word)
    synonyms = set()
    for syn_set in syn_sets or []:
        for lemma in syn_set.lemmas():
            synonyms.add(lemma.name())
    return synonyms
'''

@app.route('/')
def index():
    return 'Welcome to WordsWordsWords,\n a Shakespeare Markov Chain API'

@app.route('/words/<word>')
def words(word):
    word_regex = re.compile(re.escape(word), re.IGNORECASE)
    word_relation = db.freqs.find_one({'word': word_regex})

    if not word_relation:
        # Sample random documents from database
        rand_relations = db.freqs.aggregate([{'$sample': {'size': RANDOM_SIZE}}])
        # Extract the 'word' property from each of the documents
        word_list = [rand_relation['word'] for rand_relation in rand_relations]
        return jsonify(word_list)

    # Extract the list of words and frequencies from this word's relations
    freq_pairs = word_relation['freqs']
    # Sort in descending order of frequency
    freq_pairs.sort(key=lambda f: -f['freq'])
    # Extract the 'word' property from each of the records
    word_list = [freq_pair['word'] for freq_pair in freq_pairs]
    return jsonify(word_list)

@app.route('/starters')
def starters():
    rand_words = db.starters.aggregate([{'$sample': {'size': 20}}])
    # Extract 'word' property of each of the queried documents
    word_list = [word['word'] for word in rand_words]
    return jsonify(word_list)

@app.route('/<other>')
def handleIllegalRequest(other):
    return "405: Restricted method"

@app.route('/ping')
def ping():
    return "on database: " + db.name
