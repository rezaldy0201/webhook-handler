from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ✅ Token Telegram diambil dari ENV
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN belum disetel di environment!")

# ✅ URL API Telegram
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# ✅ Fungsi umum untuk mengirim balasan
def kirim_balasan(chat_id, text, reply_to_message_id=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id

    try:
        res = requests.post(f"{TELEGRAM_API_URL}/sendMessage", json=payload)
        res.raise_for_status()
        print("✅ Balasan berhasil dikirim:", res.json())
    except requests.exceptions.RequestException as e:
        print("❌ Gagal mengirim balasan:", e)

# ✅ Webhook Handler
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.get_json()
    print("📩 Webhook diterima:", data)

    if 'message' in data:
        msg = data['message']
        chat_id = msg['chat']['id']
        text = msg.get('text', '')
        message_id = msg.get('message_id')

        # Balas pesan
        reply_text = f"Halo Ayah 👋\nKamu mengirim: {text}"
        kirim_balasan(chat_id, reply_text, reply_to_message_id=message_id)

    elif 'callback_query' in data:
        callback = data['callback_query']
        data_cb = callback['data']
        chat_id = callback['message']['chat']['id']
        message_id = callback['message']['message_id']

        if data_cb.startswith("EXECUTE"):
            _, symbol, sinyal, conf, harga = data_cb.split("|")
            reply = f"✅ Eksekusi untuk *{symbol}* telah dikonfirmasi."
        elif data_cb.startswith("IGNORE"):
            _, symbol = data_cb.split("|")
            reply = f"❌ Sinyal *{symbol}* telah diabaikan."
        else:
            reply = "⚠️ Callback tidak dikenal."

        kirim_balasan(chat_id, reply, reply_to_message_id=message_id)

    return "OK", 200

# ✅ Jalankan server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
