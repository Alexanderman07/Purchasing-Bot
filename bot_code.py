import requests
import json
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

headers = {}

mobile_emulator = {}

prefs = {}

driver = webdriver.Chrome(executable_path='')


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

def get_color(item_id, color, size):
    URL = f'/{item_id}'
    html = requests.get(url=URL)
    output = json.loads(html.text)

    for product_color in output['styles']:
        if color in product_color['name']:
            for product_size in product_color['sizes']:
                if size in product_size['name']:
                    return product_color['id'] 

if __name__ == '__main__':
    item_id = find_item('Logo Split')
    color_id = get_color(item_id, 'Black', "Large")
    print(color_id)
