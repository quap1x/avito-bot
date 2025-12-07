from flask import Flask, request
import requests
import telegram
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
AVITO_CLIENT_ID = os.environ.get("AVITO_CLIENT_ID")
AVITO_CLIENT_SECRET = os.environ.get("AVITO_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

bot = telegram.Bot(token=TELEGRAM_TOKEN)
app = Flask(__name__)

user_chat_id = {}

@app.route('/start', methods=['POST'])
def telegram_webhook():
    data = request.json
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')
        user_chat_id['admin'] = chat_id
        if text == "/start":
            auth_url = (
                f"https://avito.ru/oauth?"
                f"client_id={AVITO_CLIENT_ID}"
                f"&response_type=code"
                f"&redirect_uri={REDIRECT_URI}"
            )
            bot.send_message(chat_id, f"Войди в Авито:\n{auth_url}")
    return "ok"

@app.route('/avito/callback')
def avito_callback():
    code = request.args.get('code')
    token_res = requests.post("https://api.avito.ru/token", data={
        'client_id': AVITO_CLIENT_ID,
        'client_secret': AVITO_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    })
    bot.send_message(user_chat_id['admin'], "✅ Авито подключено!")
    return "OK"

@app.route('/avito/webhook', methods=['POST'])
def avito_webhook():
    data = request.json
    text = data.get("message", {}).get("text", "Новое сообщение")
    bot.send_message(user_chat_id['admin'], f"📩 Авито:\n{text}")
    return "ok"

@app.route("/")
def index():
    return "Bot is running"

if name == '__main__':
    app.run(host="0.0.0.0", port=10000)