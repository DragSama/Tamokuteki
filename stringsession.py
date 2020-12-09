from telethon.sync import TelegramClient
from telethon.sessions import StringSession

print("""KEEP THE STRING YOU GET FROM THIS SECRET.""")

APP_ID = int(input("Enter APP ID here: "))
API_HASH = input("Enter API HASH here: ")

with TelegramClient(StringSession(), APP_ID, API_HASH) as client:
    print("--------------------")
    print(client.session.save())
    print("--------------------")
