import flask
import telebot
import conf
import re

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)

bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

def wordcount(text):
    text1 = text.replace('.', ' ')
    text1 = text1.replace('!', ' ')
    text1 = text1.replace(',', ' ')
    text1 = text1.replace('?', ' ')
    text1 = text1.replace('+', '')
    text1 = text1.replace(')', ' ')
    text1 = text1.replace('-', '')
    text1 = text1.strip(' ')
    text1 = text1.replace('(', ' ')
    text1 = text1.replace('"', ' ')
    myre = re.compile(u'['u'\U0001F300-\U0001F64F'u'\U0001F680-\U0001F6FF'u'\u2600-\u26FF\u2700-\u27BF]+', re.UNICODE)
    text1 = myre.sub('', text1)
    for smth in range(0,20):
        text1 = text1.replace('  ', ' ')
    textarr = text1.split(' ')
    return len(textarr)
    
def mystemit(text):
	

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Здравствуйте! Это Мотин супербот, который считает количество слов в вашем сообщении.")


@bot.message_handler(func=lambda m: True)
def send_len(message):
	bot.send_message(message.chat.id, 'Количество слов в вашем сообщении: {}'.format(wordcount(message.text)))

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)