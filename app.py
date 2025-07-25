from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    print("📩 Webhook diterima:", data)

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        reply = f"Halo 👋 Kamu mengirim: {text}"
        kirim_balasan(chat_id, reply)

    return "OK", 200

def kirim_balasan(chat_id, text):
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(TELEGRAM_URL, json=payload)
    print("✅ Balasan dikirim:", response.json())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
