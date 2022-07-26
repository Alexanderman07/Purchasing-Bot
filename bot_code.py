import requests
import json

def find_item(name):
    URL = ''
    html = requests.get(url=URL)
    term = json.loads(html.text)
    
    for category in term['products_and_categories']:
        for item in category:
            if name in item['name']:
                print(item['name'])
                return item['id']

find_item('Logo Split')