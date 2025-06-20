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
    The user shared something that happened. Interpret it as a clear, exciting *sign* that their bigger goals are materializing.

    Tone: Future-focused, confident, imaginative.
    Style: 1–2 punchy sentences, emotionally vivid.
    Avoid: vague affirmations, abstract energy talk, or poetic metaphors.
    You can compliment the user too
    User event: "{user_input}"

    What's the bigger sign or breakthrough this points to?
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
    
    print("DeepSeek response:", response.text)  # <-- Add this!


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

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)