from itertools import product
from h11 import PRODUCT_ID
import requests
import json
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

headers = {'user-agent': 'Mozilla/5.0 (iphone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                         'like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}

mobile_emulator = {"deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
                "UserAgent": "Mozilla/5.0 (iphone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                             "Version/13.0.3 Mobile/15E148 Safari/604.1"}

prefs = {'disk-cache-size': 4096}

options = Options()
options.add_experimental_option("mobileEmulation", mobile_emulator)
options.add_experimental_option('prefs', prefs)
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options = options, executable_path='')
wait = WebDriverWait(driver, 10)

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

def get_product(item_id, color_id, size):
    URL = '' + str(item_id) + '/' + str(color_id)
    driver.get(URL)
    wait.until(EC.presence_of_all_elements_located((By.ID, 'size-opyioms')))

    options = Select(driver.find_element_by_id('size-options'))
    options.select_by_visible_text(size)

    driver.find_element_by_xpath('').click()

def checkout():
    URL = ''
    driver.get(URL)
    wait.until(EC.presence_of_all_elements_located((By.ID, 'order_billing_name')))
    driver.execute_script(f'document.getElementById("order_billing_name").value = "{}";')
    driver.execute_script(f'document.getElementById("order_email").value = "{}";')
    driver.execute_script(f'document.getElementById("order_tel").value = "{}";')
    driver.execute_script(f'document.getElementById("order_billing_address").value = "{}";')
    driver.execute_script(f'document.getElementById("order_billing_address_2").value = "{}";')
    driver.execute_script(f'document.getElementById("order_billing_address_3").value = "{}";')
    driver.execute_script(f'document.getElementById("order_billing_city").value = "{}";')
    driver.execute_script(f'document.getElementById("order_billing_zip").value = "{}";')
    driver.execute_script(f'document.getElementById("credit_card_number").value = "{}";')
    driver.execute_script(f'document.getElementById("credit_card_cvv").value = "{}";')

    card_type = Select(driver.find_element_by_id('credit_card_type'))
    card_type.select_by_visible_text()
    card_month = Select(driver.find_element_by_id('credit_card_month'))
    card_month.select_by_value()
    card_year = Select(driver.find_element_by_id('credit_card_year'))
    card_year.select_by_value()

    driver.find_element_by_id('order_terms').click()
    driver.find_element_by_id('submit_button').click()



if __name__ == '__main__':
    item_id = find_item('Logo Split')
    color_id = get_color(item_id, 'Black', "Large")
    get_product(item_id, color_id, 'Large')
