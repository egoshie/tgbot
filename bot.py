import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from flask import Flask

# --- Flask health check ---
app = Flask(__name__)

@app.route("/")
def health_check():
    return "OK", 200

# --- Telegram Bot ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = 19596916  # senin API_ID
API_HASH = "5d08627e352b240114127ffa29d486a8"  # senin API_HASH

app_client = Client(
    "vc_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- PyTgCalls (sesli sohbet) ---
voice_client = PyTgCalls(app_client)

# Basit bir /start komutu
@app_client.on_message(filters.command("start"))
async def start_bot(client, message):
    await message.reply_text("🎵 Sesli bot aktif! Müzik oynatmak için VC’ye katılın.")

# VC’ye join ve test komutu
@app_client.on_message(filters.command("join"))
async def join_vc(client, message):
    chat_id = message.chat.id
    try:
        await voice_client.join_group_call(chat_id, None)
        await message.reply_text("✅ VC’ye katıldım!")
    except Exception as e:
        await message.reply_text(f"❌ Hata: {e}")

# Bot başlatma
if __name__ == "__main__":
    import threading

    # Flask serveri ayrı thread'te çalıştır
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()

    # Telegram botu çalıştır
    app_client.run()
