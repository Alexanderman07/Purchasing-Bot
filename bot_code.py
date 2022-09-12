from itertools import product
from h11 import PRODUCT_ID
import requests
import json
import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from config import ProductDetails, UserDetails, PaymentDetails

headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                         'like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}

mobile_emulation = {
    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                 "Version/13.0.3 Mobile/15E148 Safari/604.1"}

prefs = {'disk-cache-size': 4096}

options = Options()
options.add_experimental_option("mobileEmulation", mobile_emulation)
options.add_experimental_option('prefs', prefs)
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options = options, executable_path=r"")
wait = WebDriverWait(driver, 10)

def find_item(name):
    url = 'https://www.supremenewyork.com/mobile_stock.json'
    html = requests.get(url=url)
    output = json.loads(html.text)
    
    for category in output['products_and_categories']:
        for item in output['products_and_categories'][category]:
            if name in item['name']:
                print(item['name'])
                print(item['id'])
                return item['id']

def get_color(item_id, color, size):
    url = f'https://www.supremenewyork.com/shop/{item_id}.json'
    html = requests.get(url=url)
    output = json.loads(html.text)

    for product_color in output['styles']:
        if color in product_color['name']:
            for product_size in product_color['sizes']:
                if size in product_size['name']:
                    return product_color['id'] 

def get_product(item_id, color_id, size):
    url = 'https://www.supremenewyork.com/mobile/#products/' + str(item_id) + '/' + str(color_id)
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.ID, 'size-options')))

    options = Select(driver.find_element(By.ID, 'size-options'))
    options.select_by_visible_text(size)

    driver.find_element(By.XPATH, '//*[@id="cart-update"]/span').click()

def checkout():
    time.sleep(0.5)
    url = 'https://www.supremenewyork.com/mobile/#checkout'
    driver.get(url)
    wait.until(EC.presence_of_all_elements_located((By.ID, 'order_billing_name')))
    driver.execute_script(f'document.getElementById("order_billing_name").value = "{UserDetails.NAME}";')
    driver.execute_script(f'document.getElementById("order_email").value = "{UserDetails.EMAIL}";')
    driver.execute_script(f'document.getElementById("order_tel").value = "{UserDetails.TELE}";')
    driver.execute_script(f'document.getElementById("order_billing_address").value = "{UserDetails.ADDRESS1}";')
    driver.execute_script(f'document.getElementById("order_billing_address_2").value = "{UserDetails.ADDRESS2}";')
    driver.execute_script(f'document.getElementById("order_billing_city").value = "{UserDetails.CITY}";')
    driver.execute_script(f'document.getElementById("order_billing_zip").value = "{UserDetails.ZIP}";')
    driver.execute_script(f'document.getElementById("credit_card_number").value = "{PaymentDetails.CARD_NUMBER}";')
    driver.execute_script(f'document.getElementById("credit_card_verification_value").value = "{PaymentDetails.CVV}";')

    local_state = Select(driver.find_element(By.ID, 'order_billing_state'))
    local_state.select_by_value(str(UserDetails.STATE))
    card_month = Select(driver.find_element(By.ID, 'credit_card_month'))
    card_month.select_by_value(str(PaymentDetails.MONTH))
    card_year = Select(driver.find_element(By.ID, 'credit_card_year'))
    card_year.select_by_value(str(PaymentDetails.YEAR))

    driver.find_element(By.ID, 'order_terms').click()
    driver.find_element(By.ID, 'submit_button').click()



if __name__ == '__main__':
    t0 = time.time()
    item_id = find_item(ProductDetails.KEYWORDS)
    color_id = get_color(item_id, ProductDetails.COLOR, ProductDetails.SIZE)
    get_product(item_id, color_id, ProductDetails.SIZE)
    time.sleep(0.5)
    checkout()
    print('TIME: ', time.time()-t0)
    time.sleep(100)
    
