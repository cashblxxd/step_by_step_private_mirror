from telethon.sync import TelegramClient
from json import load, dump
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()
API_ID, API_HASH = os.getenv("API_ID"), os.getenv("API_HASH")
PRIVATE_CHAT_ID, REDIRECT_CHAT_ID = int(os.getenv("PRIVATE_CHAT_ID")), int(os.getenv("REDIRECT_CHAT_ID"))
print("STARTED", datetime.now())
with TelegramClient('MyApp', API_ID, API_HASH) as client:
    with open("last_message_id.json", "r+") as f:
        s = load(f)
        last_id = s["id"]
        for message in client.iter_messages(PRIVATE_CHAT_ID, offset_id=s["id"], reverse=True):
            last_id = message.id
            if message.message:
                text = message.message
                client.send_message(REDIRECT_CHAT_ID, message=text)
            if message.photo:
                filepath = client.download_media(message)
                client.send_file(REDIRECT_CHAT_ID, filepath)
                os.remove(filepath)
    with open("last_message_id.json", "w+") as f:
        dump({"id": last_id}, f)
    
