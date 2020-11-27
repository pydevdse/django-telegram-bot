from django.shortcuts import render, HttpResponse
import time, json, requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django_telegram_bot import config
from django.views.decorators.csrf import csrf_exempt

KEY = config.TELEGRAM_KEY
URL='https://api.telegram.org/bot'+KEY+'/'

def sendd_message(chat_id, text = 'bla bla bla'):#filename='screenshot1.png'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()

def sendd_photo(chat_id, filename='screenshot.png'):
    with open(filename, "rb") as binary_file:
        url = URL + 'sendDocument'
        files = {'document': binary_file}
        data = {'chat_id' : chat_id}
        r = requests.post(url,  data=data, files = files)
    return r.json()

def screen_scr(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    try:
        driver.get(url)
    except:
        print('url bad')
        driver.quit()
        return False
    time.sleep(2)
    driver.maximize_window()
    height = driver.execute_script("return document.body.scrollHeight")
    print (height)
    driver.set_window_size(1920, height)
    time.sleep(2)
    driver.save_screenshot("screenshot.png")
    driver.quit()
    return True

@csrf_exempt
def telegram_scr(request):
    print('host:', request.META['HTTP_HOST'])
    if request.method == 'POST':
        r = json.loads(request.body.decode("utf-8"))
        chat_id = r['message']['chat']['id']
        message = r['message']['text']
        if not screen_scr(message):
            sendd_message(chat_id, 'URL BAD')
            return HttpResponse('<h2>Telegram bot</h2>')
        s  = sendd_photo(chat_id)
        print('chat_id', chat_id)
        print(s)

    return  HttpResponse ('<h2>Telegram bot</h2>')