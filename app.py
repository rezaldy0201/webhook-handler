from flask import Flask, request
import os
import requests

app = Flask(name)

def kirim_balasan(chat_id, message_id, text, token):
    url = f"https://api.telegram.org/bot{token}/editMessageText"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    data = request.json
    print("📩 Webhook diterima:", data)

    if "callback_query" in data:
        callback = data["callback_query"]
        data_cb = callback.get("data", "")
        chat_id = callback["message"]["chat"]["id"]
        message_id = callback["message"]["message_id"]

        token = os.getenv("TELEGRAM_TOKEN")
        if not token:
            print("❌ TELEGRAM_TOKEN tidak ditemukan!")
            return "Token tidak tersedia", 400

        if data_cb.startswith("EXECUTE"):
            try:
                _, symbol, sinyal, conf, harga = data_cb.split("|")
                kirim_balasan(chat_id, message_id, f"✅ Eksekusi untuk *{symbol}* arah *{sinyal}* dengan confidence *{conf}%*", token)
            except Exception as e:
                print("❌ Gagal parsing EXECUTE:", e)
        elif data_cb.startswith("IGNORE"):
            try:
                _, symbol = data_cb.split("|")
                kirim_balasan(chat_id, message_id, f"🚫 Entry *{symbol}* telah diabaikan.", token)
            except Exception as e:
                print("❌ Gagal parsing IGNORE:", e)

    return "OK", 200
