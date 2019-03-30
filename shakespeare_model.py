from collections import defaultdict
import json
import re

from bs4 import BeautifulSoup
import requests


# \w+(?:\'\w+)?(?:-\w+(?:\'\w+)?)*|(?:[.,:;!\'"()\[\]–—]|--)
word_pattern = \
    re.compile(r'\w+(?:\'\w+)?(?:-\w+(?:\'\w+)?)*|(?:[.,:;!?–—]|-{2,})')
end_word_pattern = re.compile(r'[.,:;!?–—]|-{2,}')


def is_end_word(word):
    return end_word_pattern.fullmatch(word)


def make_markov_model(words):
    if not words:
        return {}
    words = [word.lower() for word in words if word != 'I']
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
    # {'word': 'a', 'freqs': [{'word': 'b', 'freq': 0.333}, {'word': 'd', 'freq': 0.666}]}
    freqs = []
    for word, occ_dict in grams.items():
        total_occ = sum(occ_dict.values())
        freqs.append({'word': word, 'freqs': [{'word': word, 'freq': count / total_occ} for word, count in occ_dict.items()]})
    return ([{'word': word} for word in starters], freqs)


def scrape_shakespeare():
    URL = 'http://shakespeare.mit.edu/index.html'
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')

    workLinks = []

    print('Gathering URLs to scrape...')
    for a in soup.find_all('a', href=True):
        if 'index' in a['href']:
            link = 'http://shakespeare.mit.edu/' + \
                a['href'].replace('/index.html', '/full.html')
            workLinks.append(link)

    words = []
    for workURL in workLinks:
        print('Scraping ' + workURL)
        req = requests.get(workURL)
        soup = BeautifulSoup(req.content, 'html5lib')
        for a in soup.find_all('blockquote'):
            text = a.get_text().rstrip()
            words.extend(word_pattern.findall(text))

    return words


def update_db(db):
    words = scrape_shakespeare()
    starters, freqs = make_markov_model(words)
    db.freqs.insert_many(freqs)
    db.starters.insert_many(starters)


def main():
    print('Scraping...')
    words = scrape_shakespeare()
    print('Done scraping')
    print('-----------------------')
    print('Building model...')
    starters, freqs = make_markov_model(words)
    print('Done building model')
    print('-----------------------')
    print('Writing to files...')
    print('Writing starters.json')
    with open('starters.json', 'w') as starters_file:
        json.dump(starters, starters_file)
    print('Wrote starters.json')
    print('Writing freqs.json')
    with open('freqs.json', 'w') as freqs_file:
        json.dump(freqs, freqs_file)
    print('Wrote freqs.json')
    print('Done')

if __name__ == '__main__':
    main()
