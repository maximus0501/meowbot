import requests
import time

API_URL = 'https://api.telegram.org/bot'
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
API_DOGS_URL = 'https://api.thedogapi.com/v1/images/search'
BOT_TOKEN = '<your_token>'
ERROR_TEXT = 'Извини, на нашем сервере сбой :( Попробуй позже'
USER_ERR_TEXT = 'Извини, я тебя не понял uwu Нажми /help, если нужна помощь (мяяяу)'
HELP_TEXT = '''
Привет! Это МЯУ БОТ!
Я могу отправлять тебе смешных котиков и собачек, если тебе грустно :)
Команды:
/start - запуск
/help - помощь
/cat - кошечка (мяяяяяу UwU)
/dog - собачка (гав гав 0w0)'''
offset = -2
counter = 0
cat_response: requests.Response
dog_response: requests.Response
cat_link: str
dog_link: str

while True:
    print('attempt =', counter)
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            if result.get('message', 0) != 0:
                offset = result['update_id']
                chat_id = result['message']['from']['id']
                msg_text = result['message']['text']
                cat_response = requests.get(API_CATS_URL)
                dog_response = requests.get(API_DOGS_URL)
                if msg_text in ('/cat', '/dog'):
                    if cat_response.status_code == 200 and msg_text == '/cat':
                        cat_link = cat_response.json()[0]['url']
                        requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}')
                    elif dog_response.status_code == 200 and msg_text == '/dog':
                        dog_link = dog_response.json()[0]['url']
                        requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={dog_link}')
                    else:
                        requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')
                elif msg_text == '/help' or msg_text == '/start':
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={HELP_TEXT}')
                else:
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={USER_ERR_TEXT}')

    time.sleep(1)
    counter += 1
