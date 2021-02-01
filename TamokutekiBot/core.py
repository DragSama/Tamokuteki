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

from TamokutekiBot.helpers import command
from pathlib import Path
import re


@Tamokuteki.on(command(pattern="load"))
async def loading(event):
    reply = await event.get_reply_message()
    if reply:
        if reply.media and reply.media.document:
            if reply.media.document.mime_type == "text/x-python":
                path = await Tamokuteki.download_media(reply, "plugins/")
            else:
                await event.send("Reply to a valid file.")
                return
    else:
        if len((split := event.text.split(" ", 1))) == 1:
            await event.send("Reply to a plugin.")
            return
        path = split[1] + ".py"
        path = Path(__file__).parent / "plugins" / path
    try:
        Tamokuteki.load_plugin(path)
    except Exception as e:
        await event.send(str(e))
        return
    await event.send("Loaded plugin " + path)


@Tamokuteki.on(command(pattern="unload"))
async def unloading(event):
    try:
        mod = event.text.split(" ", 1)[1]
    except:
        return
    Tamokuteki.unload_plugin(mod)
    await event.send("Unloaded plugin " + mod)


@Tamokuteki.on(command(pattern="plugins"))
async def lplugins(event):
    plugins = Tamokuteki.list_plugins()
    msg = "Currently loaded plugins:\n\n"
    for plugin in plugins:
        msg += f"- `{plugin}`\n"
    await event.send(msg)


__commands__ = {
    "load": "Load a plugin. Format: .load <plugin name>",
    "unload": "Unload a plugin. Format: .unload <plugin name>",
    "plugins": "List all loaded plugins.",
    "description": "[Core plugin]",
}
