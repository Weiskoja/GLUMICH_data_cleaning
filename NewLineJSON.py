import json

with open('data-wrangling/done/Fish.json') as f:
    data = json.load(f)

with open('ndjson.json', 'w') as f:
    for obj in data:
        f.write(json.dumps(obj) + '\n')

