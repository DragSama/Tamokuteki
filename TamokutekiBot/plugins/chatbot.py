# Copyright (C) 2020-2021 DragSama. All rights reserved. Source code available under the AGPL.
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

# Uses Coffehouse API: https://coffeehouse.intellivoid.net/

from coffeehouse.lydia import LydiaAI
from telethon import events
from TamokutekiBot import COLLECTION, COFFEEHOUSE_ACCESS_KEY
from TamokutekiBot.helpers import command

import asyncio
import time

if COLLECTION:
    lydia = LydiaAI(COFFEEHOUSE_ACCESS_KEY)

    async def get_settings():
        data = await COLLECTION.find_one({"type": "lydia-settings"})
        return data

    async def update_settings(new_settings):
        await COLLECTION.replace_one(await get_settings(), new_settings)

    async def get_data():
        data = await get_settings()
        if not data:
            data = {"type": "lydia-settings", "users": {}}
            await COLLECTION.insert_one(data)
        return data

    @Tamokuteki.on(command(pattern="addchat", outgoing=True))
    async def addchat(event):
        settings = await get_data()
        reply_msg = await event.get_reply_message()
        if not reply_msg:
            await event.edit("Reply to a user to enable chatbot for it.")
            return
        user_id = reply_msg.sender_id
        if user_id in settings["users"]:
            await event.edit("Chatbot is already enabled for this chat.")
            return
        session = lydia.create_session()
        settings["users"][str(user_id)] = {
            "expires_at": session.expires,
            "session_id": session.id,
        }
        await update_settings(settings)
        await event.edit("Enabled!")

    @Tamokuteki.on(command(pattern="rmchat", outgoing=True))
    async def rmchat(event):
        settings = await get_data()
        reply_msg = await event.get_reply_message()
        if not reply_msg:
            await event.edit("Reply to a user to enable chatbot for it.")
            return
        user_id = reply_msg.sender_id
        if user_id not in settings["users"]:
            await event.edit("Chatbot is not enabled for this chat.")
            return
        del settings["users"][str(user_id)]
        await update_settings(settings)
        await event.edit("Disabled!")

    @Tamokuteki.on(command(pattern="listchats", outgoing=True))
    async def listchats(event):
        settings = await get_data()
        msg = "List of chats:\n"
        for user in settings["users"]:
            msg += f"• {user}\n"
        await event.edit(msg)

    @Tamokuteki.on(events.NewMessage(incoming=True, func=lambda event: event.mentioned))
    async def process_replies(event):
        if (
            event.fwd_from
            or event.media
            or not (str(event.sender_id) in (await get_data())["users"])
        ):
            return
        print("Replying to user: " + str(event.sender_id))
        data = await get_data()
        user = data["users"][str(event.sender_id)]
        message = event.text

        if user["expires_at"] < time.time():
            session = lydia.create_session()
            data["users"][str(event.sender_id)] = {
                "expires_at": session.expires,
                "session_id": session.id,
            }
            await update_settings(data)
            output = lydia.think_thought(session.id, message)
        else:
            output = lydia.think_thought(user["session_id"], message)

        async with Tamokuteki.action(event.chat_id, "typing"):
            await asyncio.sleep(0.2)
            await event.reply(output)

    __commands__ = {
        "addchat": "Enable chatbot for a user",
        "rmchat": "Disable chatbot for a user",
        "listchats": "List all users which you have enabled chatbot for.",
        "description": "Uses Coffehouse API: https://coffeehouse.intellivoid.net",
    }
