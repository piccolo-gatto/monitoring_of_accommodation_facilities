from selenium import webdriver
from selenium.webdriver.common.by import By
# from multiprocessing.dummy import Pool
# from multiprocessing import cpu_count, freeze_support
import time
import requests
import random
import tqdm
import pandas as pd
import os

all_services = pd.read_csv('services.csv')


def get_urls(url: str):
    urls = []
    driver = webdriver.Chrome()
    driver.get(url)
    try:
        driver.find_element(by=By.CLASS_NAME, value='styles-module-closeButton-sE_e_').click()
    except:
        pass
    time.sleep(random.randint(5, 10))
    pages = int(driver.find_elements(by=By.CLASS_NAME, value='styles-module-text-_KauC')[-1].text)
    for i in tqdm.tqdm(range(1, pages + 1)):
        driver.get(url + f'&p={i}')
        cards = driver.find_elements(by=By.CLASS_NAME, value='iva-item-content-rejJg')
        for card in cards:
            try:
                card_url = card.find_element(by=By.TAG_NAME, value='a').get_attribute(name='href')
                checker = requests.post('http://server:8000/duplicates', json={'url': card_url}).json()
                if checker['message'] == 'None':
                    urls.append(card_url)
                else:
                    continue
            except:
                continue
    driver.quit()
    return urls


def parse_data(urls):
    for url in urls:
        info = {'url': '',
                'type': '',
                'address': '',
                'lat': 0.0,
                'lon': 0.0
                }
        prices = {
            'price': 0
        }
        driver = webdriver.Chrome()
        driver.get(url)
        info['url'] = url
        try:
            price_div = driver.find_element(by=By.CLASS_NAME, value='style-item-price-PuQ0I')
            if 'от' in price_div.text.lower():
                prices['price'] = int(driver.find_element(by=By.XPATH,
                value='//*[@id="app"]/div/div[3]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div/div/div[1]/div/div/div/div/div/span/span/span[2]').get_attribute(
                'content'))
            else:
                prices['price'] = int(driver.find_element(by=By.XPATH,
                value='//*[@id="app"]/div/div[3]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div/div/div[1]/div/div/div/div/div/span/span/span[1]').get_attribute(
                'content'))
        except:
            prices['price'] = 0
        try:
            info['address'] += driver.find_element(by=By.CLASS_NAME, value='style-item-address__string-wt61A').text
        except:
            continue
        try:
            header = driver.find_element(by=By.CLASS_NAME, value='style-titleWrapper-Hmr_5').text
            if 'квартира' in header.lower():
                info['type'] = 'Квартира'
            else:
                info['type'] += header.split(' ')[0]
        except:
            continue
        try:
            geo = driver.find_element(by=By.CLASS_NAME, value='style-item-map-wrapper-ElFsX')
            info['lat'] += float(geo.get_attribute('data-map-lat'))
            info['lon'] += float(geo.get_attribute('data-map-lon'))
        except:
            continue

        house_response = requests.post(url="http://server:8000/add_house", json=info).json()
        json_response = dict(house_response)
        prices['house_id'] = int(json_response['id'])
        try:
            params = driver.find_elements(by=By.CLASS_NAME, value='params-paramsList-_awNW')[0].text
            description = driver.find_element(by=By.CLASS_NAME, value='style-item-description-pL_gy').text
            for index, service in all_services.iterrows():
                if (service['name'][: -1] in params.lower()) or (service['name'][: -1] in description.lower()):
                    avito_services = {
                        'house_id': int(json_response['id']),
                        'service_type': service['type'],
                        'name': service['name']
                    }
                    requests.post(url="http://server:8000/add_service", json=avito_services)

        except:
            pass
        requests.post(url="http://server:8000/add_price", json=prices)
        time.sleep(random.randint(5, 20))
        driver.quit()


def avito_data(url: str):
    urls = get_urls(url)
    # cpucount = cpu_count()
    # if len(urls) > cpucount - 1:
    #     iterations = len(urls) / float(cpucount)
    # else:
    #     iterations = len(urls)
    # for i in tqdm.tqdm(range(0, cpucount)):
    #     freeze_support()
    #     pool = Pool()
    #     start = int(iterations * i)
    #     end = int(iterations * (i + 1))
    #     res = pool.apply_async(parse_data, [urls[start:end]])
    #     res.get()
    #     pool.terminate()
    for url in tqdm.tqdm(urls):
        parse_data(url)


