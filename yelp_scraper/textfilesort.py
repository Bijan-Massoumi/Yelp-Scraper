import json

filename = "crawled_data/Fremont_items.json"
itemList = []
with open(filename) as f:
    for line in f:
        itemList.append(json.loads(line))
itemList = sorted(itemList, key=lambda k: k['url'])

file = open(filename 'wb')
for item in itemList:
    line = json.dumps(dict(item)) + "\n"
    self.file.write(line)
