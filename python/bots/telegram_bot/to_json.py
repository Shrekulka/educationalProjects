# telegram_bot/to_json.py

import json

ar = []
with open('cenz.txt', encoding='UTF-8') as r:
    for i in r:
        n = i.lower().split('\n')[0]
        if n != '':
            ar.append(n)
with open('cenz.json', 'w', encoding='UTF-8') as e:
    json.dump(ar, e)
