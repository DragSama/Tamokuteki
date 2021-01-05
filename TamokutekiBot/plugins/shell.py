# Copyright (C) 2021 DragSama. All rights reserved. Source code available under the AGPL.
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

from telethon import events
import asyncio
import io


@Tamokuteki.on(events.NewMessage(pattern="\.(term|terminal|sh|shell) ", outgoing=True))
async def shell(event):
    if event.fwd_from:
        return
    cmd = event.text.split(" ", 1)
    if len(cmd) == 1:
        return
    else:
        cmd = cmd[1]
    async_process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await async_process.communicate()
    msg = f"**Command:**\n`{cmd}`\n"
    if stderr.decode():
        msg += f"**Stderr:**\n`{stderr.decode()}`"
    if stdout.decode():
        msg += f"**Stdout:**\n`{stdout.decode()}`"
    if len(msg) > 4096:
        with io.BytesIO(msg) as file:
            file.name = "shell.txt"
            await Tamokuteki.send_file(
                event.chat_id,
                file,
                force_document=True,
                caption=cmd,
                reply_to=event.message.id,
            )
            return
    await event.edit(msg)


__commands__ = {"shell": "Run command"}
