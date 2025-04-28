import os
import openai
from flask import Flask, request
import telegram

TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telegram.Bot(token=TOKEN)
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    if update.message:
        text = update.message.text
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": text}]
        )
        bot.send_message(
            chat_id=update.message.chat_id,
            text=response['choices'][0]['message']['content']
        )
    return 'ok'

@app.route('/')
def index():
    return 'LightMind Helper Bot is running!'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
