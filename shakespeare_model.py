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
    starters = set()
    enders = set()
    # {'a': {('b', 'c'): 1, ('d', 'e'): 2}}
    grams = defaultdict(lambda: defaultdict(int))
    last_was_end = True
    for word in words:
        if is_end_word(word):
            enders.add(word)
        elif last_was_end:
            starters.add(word)
            last_was_end = False
    for i in range(len(words) - 2):
        grams[words[i]][(words[i + 1], words[i + 2])] += 1
    # {'a': [{'words': ['b', 'c'], 'freq': 0.333}, {'words': ['d', 'e'], 'freq': 0.666}]}
    freqs = {}
    for word, occ_dict in grams.items():
        total_occ = sum(occ_dict.values())
        freqs[word] = [{'words': list(pair), 'freq': count / total_occ} for pair, count in occ_dict.items()]
    return {'starters': list(starters), 'enders': list(enders), 'freqs': freqs}


def scrape_shakespeare():
    URL = 'http://shakespeare.mit.edu/index.html'
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')

    workLinks = []

    for a in soup.find_all('a', href=True):
        if 'index' in a['href']:
            link = 'http://shakespeare.mit.edu/' + \
                a['href'].replace('/index.html', '/full.html')
            workLinks.append(link)

    words = []
    for workURL in workLinks:
        req = requests.get(workURL)
        soup = BeautifulSoup(req.content, 'html5lib')
        for a in soup.find_all('blockquote'):
            text = a.get_text().rstrip()
            words.extend(word_pattern.findall(text))

    return words


def main():
    print('Scraping:')
    words = scrape_shakespeare()
    print('Building model:')
    model = make_markov_model(words)
    print('Dumping:')
    print(json.dumps(model))


if __name__ == '__main__':
    main()
