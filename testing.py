#Python program to scrape website
#and save quotes from website
import requests
from bs4 import BeautifulSoup
import re


URL = "http://shakespeare.mit.edu/index.html"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')
#print(soup.prettify())

workLinks = []
#print(wordsOnly("<a name="2.3.5">into seeming knowledge, when we should submit</a><br/>"))
for a in soup.find_all('a', href=True):
    if("index" in a['href']):
        link = "http://shakespeare.mit.edu/" + a['href'].replace("/index.html", "/full.html")
        workLinks.append(link)
        #print(link)
#allWorks = [37]
count = 0
for workURL in workLinks:
    req = requests.get(workURL)
    soup = BeautifulSoup(req.content, 'html5lib')
    blocks = []
    for a in soup.find_all('blockquote'):
        words = a.get_text().lower().rstrip()
        nopunc = re.sub(r'[^\w\s]','',words)
        blocks.append(nopunc)

    #for b in blocks:

    #print(blocks)
    #allWorks[count] = [blocks]
    #count = count + 1




