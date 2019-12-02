import json
from collections import defaultdict
from unicodedata import normalize
from bs4 import BeautifulSoup
import requests

data = defaultdict(list)

def insertEntry(state, city):
    global data
    cities = data[state]
    cities.append(city)
    data[state] = cities

url = 'https://service.unece.org/trade/locode/in.htm'

res = requests.get(url)

webpage = BeautifulSoup(res.text, 'html.parser')

tables = webpage.findAll('table')
webTable = tables[2]

for row in webTable.findChildren('tr'):
    elements = row.findChildren('td')
    city, state = normalize('NFKC', elements[2].text).strip(), \
            normalize('NFKC', elements[4].text).strip()
    insertEntry(state, city)

with open('cities.json', 'w') as f:
    f.write(json.dumps(data))
