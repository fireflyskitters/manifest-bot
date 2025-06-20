from flask import Flask, request
import requests

app = Flask(__name__)

# 🔑 Set your API keys
TELEGRAM_TOKEN = '7711605219:AAHAPlf9bSvvLfPtUk3r5vTdu3WvUYwsNxM'
DEEPSEEK_API_KEY = 'sk-930be2a0978f405ea7fde42a24127184'

# 🌐 Telegram URL for sending replies
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.route('/', methods=['POST'])
def webhook():
    data = request.json

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        user_message = data['message'].get('text', '')
        print(f"Received: {user_message}")

        reply = generate_manifest_reply(user_message)
        send_message(chat_id, reply)

    return 'ok'

def generate_manifest_reply(user_input):
    prompt = f"""
User wrote: "{user_input}"
Turn this into a positive manifestation or sign from the universe.
Make it sound warm, magical, and affirming.
"""

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 100
    }

    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    result = response.json()
    return result['choices'][0]['message']['content'].strip()

def send_message(chat_id, text):
    payload = {
        'chat_id': chat_id,
        'text': text
    }

    response = requests.post(TELEGRAM_URL, json=payload)
    if response.status_code != 200:
        print(f"Telegram error: {response.text}")