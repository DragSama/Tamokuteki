# Copyright (C) 2020 DragSama. All rights reserved. Source code available under the AGPL.
#
# This file is part of TamokutekiBot.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from TamokutekiBot.classes import TamokutekiClient
from telethon.sessions import StringSession
from motor import motor_asyncio

import logging
import os

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

if os.environ.get("ENV", False):
    API_ID = os.environ.get("API_ID")
    API_HASH = os.environ.get("API_HASH")
    STRING_SESSION = os.environ.get("STRING_SESSION")
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
    COFFEHOUSE_ACCESS_KEY = os.environ.get("COFFEHOUSE_ACCESS_KEY", None)
else:
    import TamokutekiBot.config as Config
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    STRING_SESSION = Config.STRING_SESSION
    try:
      MONGO_DB_URI = Config.MONGO_DB_URI
      COFFEHOUSE_ACCESS_KEY = Config.COFFEHOUSE_ACCESS_KEY
    except:
      COFFEHOUSE_ACCESS_KEY = None
      MONGO_DB_URI = None

if MONGO_DB_URI:
    MONGO_CLIENT = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI)
else:
    MONGO_CLIENT = None

Tamokuteki = TamokutekiClient(
    StringSession(STRING_SESSION),
    API_ID,
    API_HASH
)
