from telethon.sync import TelegramClient
from json import load, dump
from datetime import datetime
import os

API_ID="18846638"
API_HASH="26b31c20a07385d0770ce216a6f61c63"
PRIVATE_CHAT_ID=-1001332191157
REDIRECT_CHAT_ID=-1001786371730

print("STARTED", datetime.now())
client = TelegramClient('MyApp', API_ID, API_HASH)
client.start()
with open("last_message_id.json", "r+") as f:
    s = load(f)
    last_id = s["id"]
    print("last id", last_id)
    for message in client.iter_messages(PRIVATE_CHAT_ID, offset_id=s["id"], reverse=True):
        print("message id", message.id)
        last_id = message.id
        if message.message:
            text = message.message
            client.send_message(REDIRECT_CHAT_ID, message=text)
        if message.photo:
            filepath = client.download_media(message)
            client.send_file(REDIRECT_CHAT_ID, filepath)
            os.remove(filepath)
    print("last id", last_id)
with open("last_message_id.json", "w+") as f:
    dump({"id": last_id}, f)
client.disconnect()
print("DONE", datetime.now())
