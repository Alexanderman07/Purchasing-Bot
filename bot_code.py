import requests
import json

def find_item(name):
    URL = ''
    html = requests.get(url=URL)
    term = json.loads(html.text)
    print(term)

find_item(None)