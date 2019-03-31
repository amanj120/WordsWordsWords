from collections import defaultdict
import json
from multiprocessing import Pool
import re
import os
import sys

from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests

MONGO_URI = 'mongodb://admin:aaWyedsDgy03jcLc@cluster0-shard-00-00-kwnae.gcp.mongodb.net:27017,cluster0-shard-00-01-kwnae.gcp.mongodb.net:27017,cluster0-shard-00-02-kwnae.gcp.mongodb.net:27017/markov?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'
BASE_URL = 'http://shakespeare.mit.edu/index.html'
POOL_SIZE = 10

word_pattern = \
    re.compile(r'\w+(?:\'\w+)?(?:-\w+(?:\'\w+)?)*(?:\s*[.,:;!?–—]|-+)?')
end_word_pattern = \
    re.compile(r'\w+(?:\'\w+)?(?:-\w+(?:\'\w+)?)*(?:\s*[.,:;!?–—]|-+)+')


def load_presets():
    presets = {}
    try:
        print('> Loading presets...')
        with open(os.path.join(sys.path[0], 'presets.json'), 'r') as presets_file:
            presets = json.load(presets_file)
        print('> Done loading presets')
    except FileNotFoundError:
        print('> Error reading presets.json')
    return presets


def is_end_word(word):
    return end_word_pattern.fullmatch(word)


def make_markov_model(words, presets):
    if not words:
        return {}
    words = [word.lower() for word in words]
    starters = set()
    # {'a': {'b': 1, 'd': 2}}
    grams = defaultdict(lambda: defaultdict(int))
    last_was_end = True
    for word in words:
        if is_end_word(word):
            last_was_end = True
        elif last_was_end:
            starters.add(word)
            last_was_end = False
    for i in range(len(words) - 1):
        grams[words[i]][(words[i + 1])] += 1
    freqs = []
    # freqs = presets
    for word, word_freqs in presets.items():
        freqs.append({'word': word, 'freqs': word_freqs})
    # freqs = presets
    for word, occ_dict in grams.items():
        total_occ = sum(occ_dict.values())
        freqs.append({'word': word, 'freqs': [{'word': word, 'freq': count / total_occ} for word, count in occ_dict.items()]})
        # freqs[word] = [{'word': word, 'freq': count / total_occ} for word, count in occ_dict.items()]
    return [{'word': word} for word in starters], freqs


def scrapeLink(work_url):
    words = []
    print('Scraping ' + work_url)
    req = requests.get(work_url)
    soup = BeautifulSoup(req.content, 'html5lib')
    for a in soup.find_all('blockquote'):
        text = a.get_text().rstrip()
        words.extend(word_pattern.findall(text))
    return words


def scrape_shakespeare():
    r = requests.get(BASE_URL)

    soup = BeautifulSoup(r.content, 'html5lib')

    work_links = []

    print('> Gathering URLs to scrape...')
    for a in soup.find_all('a', href=True):
        if 'index' in a['href']:
            link = 'http://shakespeare.mit.edu/' + \
                a['href'].replace('/index.html', '/full.html')
            work_links.append(link)
    print('> Done gathering URLs')

    pool = Pool(POOL_SIZE)
    works = pool.map(scrapeLink, work_links)
    pool.terminate()
    pool.join()

    return [word for words in works for word in words]


def update_db(db):
    presets = load_presets()
    print('> Scraping...')
    words = scrape_shakespeare()
    print('> Done scraping')
    print('-----------------------')
    print('> Building model...')
    starters, freqs = make_markov_model(words, presets)
    print('> Done building model')
    print('-----------------------')
    print('> Inserting into database...')
    print('> Dropping starters collection...')
    db.starters.drop()
    print('> Bulk inserting starters...')
    db.starters.insert_many(starters)
    print('> Dropping freqs collection...')
    db.freqs.drop()
    print('> Bulk inserting freqs...')
    db.freqs.insert_many(freqs)
    print('> Done')


def write_files():
    presets = load_presets()
    print('> Scraping...')
    words = scrape_shakespeare()
    print('> Done scraping')
    print('-----------------------')
    print('> Building model...')
    starters, freqs = make_markov_model(words, presets)
    print('> Done building model')
    print('-----------------------')
    print('> Writing to files...')
    print('> Writing starters.json')
    with open('starters.json', 'w') as starters_file:
        json.dump(starters, starters_file)
    print('> Wrote starters.json')
    print('> Writing freqs.json')
    with open('freqs.json', 'w') as freqs_file:
        json.dump(freqs, freqs_file)
    print('> Wrote freqs.json')
    print('> Done')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == '--help':
            commands = ['help', 'write-files', 'test-db', 'sample-data', 'update-db']
            print('Possible commands:\n' + '\n'.join(['    --' + command for command in commands]))
        elif arg == '--write-files':
            write_files()
        elif arg == '--test-db':
            admin_client = MongoClient(MONGO_URI)
            print('Fetching database names:')
            print([name for name in admin_client.list_databases()])
            print('\nFetching collection names in markov:')
            print([name for name in admin_client.markov.list_collections()])
        elif arg == '--sample-data':
            admin_client = MongoClient(MONGO_URI)
            db = admin_client.markov
            rand_starters = db.starters.aggregate([{'$sample': {'size': 20}}])
            rand_freqs = db.freqs.aggregate([{'$sample': {'size': 5}}])
            print('starters\n--------------------')
            print(list(rand_starters))
            print('\nfreqs\n--------------------')
            print(list(rand_freqs))
        elif arg == '--update-db':
            admin_client = MongoClient(MONGO_URI)
            update_db(admin_client.markov)
        else:
            raise Exception('Invalid flag: ' + sys.argv[1])
