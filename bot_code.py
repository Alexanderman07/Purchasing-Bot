import requests
import json

def find_item(name):
    URL = ''
    html = requests.get(url=URL)
    term = json.loads(html.text)
    
    for category in term['products_and_categories']:
        for item in term['products_and_categories'][category]:
            if name in item['name']:
                print(item['name'])
                print(item['id'])
                return item['id']

def get_color(item_id, color):
    URL = f'/{item_id}'
    html = requests.get(url=URL)
    output = json.loads(html.text)
    print(output)

if __name__ == '__main__':
    item_id = find_item('Logo Split')
    get_color(item_id, 'Black')
