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

# Thanks to https://github.com/rsktg or @TheRealPhoenix on telegram for the idea of getrep

from TamokutekiBot.helpers import command

import asyncio
import time

@Tamokuteki.on(command(pattern="alive", outgoing=True))
async def alive(event):
    await event.edit("I'm alive!")

@Tamokuteki.on(command(pattern="repo", outgoing=True))
async def repo(event):
    await event.edit("Tamokuteki Bot\nRepo: https://github.com/DragSama/Tamokuteki")

@Tamokuteki.on(command(pattern="getrep", outgoing=True))
async def getrep(event):
    split = event.text.split(' ', 2)
    replied = await event.get_reply_message()
    if len(split) != 3 and not replied:
        await event.edit('Format: .getrep <username or id> <message to send or reply to msg>')
        return
    if len(split) == 1:
        await event.edit('Username/ID not provided')
        return
    u = int(split[1]) if split[1].isnumeric() else split[1]
    try:
        async with event.client.conversation(u, timeout = 900) as conv:
            chat = await conv.get_chat()
            if replied:
                msg = f"**Sent**:\n`Replied message`\n**To**:\n`{chat.first_name}`\n"
            else:
                msg = f"**Sent**:\n`{split[2]}`\n**To**:\n`{chat.first_name}`\n"
            await event.edit(msg)
            if replied:
                await conv.send_message(replied)
            else:
                await conv.send_message(split[2])
            start_time = time.time()
            r = await conv.get_response()
            end_time = time.time()
            await r.forward_to(event.chat_id)
            if replied:
                msg = f"**Sent**:\n`Replied message`\n**To**:\n`{chat.first_name}`\n\n**Got response in {round(end_time - start_time, 2)}s**"
            else:
                msg = f"**Sent**:\n`{split[2]}`\n**To**:\n`{chat.first_name}`\n\n**Got response in {round(end_time - start_time, 2)}s**"
            await event.edit(msg)
    except ValueError as ve:
        await event.edit(f'Error:\n{ve}')
    except asyncio.exceptions.TimeoutError:
        await event.edit(f'Timeout, Failed to get reply from {u} within given timeout')

__commands__ = {
    "config": "Get repo.",
    "alive": "Check if userbot is running.",
    "getrep": "Send a message and wait for reply. Format: .getrep <username or id> <message to send or reply to msg>"
}
