from TamokutekiBot.classes import TamokutekiClient
from telethon.sessions import StringSession

import os
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

if os.environ.get("ENV", False):
    API_ID = os.environ.get("API_ID")
    API_HASH = os.environ.get("API_HASH")
    STRING_SESSION = os.environ.get("STRING_SESSION")
else:
    import TamokutekiBot.config as Config
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    STRING_SESSION = Config.STRING_SESSION

Tamokuteki = TamokutekiClient(
    StringSession(STRING_SESSION),
    API_ID,
    API_HASH
)
print(Tamokuteki)
