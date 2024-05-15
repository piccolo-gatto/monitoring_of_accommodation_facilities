import avito as avito
import time
from flask import Flask
from flask_apscheduler import APScheduler
import uvicorn


app = Flask(__name__)
scheduler = APScheduler()

urls = ['https://www.avito.ru/irkutskaya_oblast/komnaty/sdam/posutochno/-ASgBAgICAkSQA74QqAn4YA?cd=1&context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyt1JKTixJzMlPV7KuBQQAAP__dhSE3CMAAAA&user=1',
        'https://www.avito.ru/irkutskaya_oblast/doma_dachi_kottedzhi/sdam/posutochno-ASgBAgICAkSUA9IQoAjKVQ?cd=1&context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyt1JKTixJzMlPV7KuBQQAAP__dhSE3CMAAAA&f=ASgBAgICA0SUA9IQoAjKVeb5EcSHiwM&user=1',
        'https://www.avito.ru/irkutskaya_oblast/kvartiry/sdam/posutochno/-ASgBAgICAkSSA8gQ8AeSUg?cd=1&context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyt1JKTixJzMlPV7KuBQQAAP__dhSE3CMAAAA&user=1']

@scheduler.task('cron', id='parse', hour=0, minute=0)
def parse():
    for url in urls:
        avito.avito_data(url)
        time.sleep(60)


if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    uvicorn.run(app, host='0.0.0.0', port=8005)
