from TamokutekiBot.helpers import command
from pathlib import Path
import re

@Tamokuteki.on(command(pattern = "load"))
async def loading(event):
    reply = await event.get_reply_message()
    if reply:
        if reply.media and reply.media.document:
            if reply.media.document.mime_type == "text/x-python":
                path = await Tamokuteki.download_media(reply)
            else:
                await event.edit("Reply to a valid file.")
                return
    else:
        if len((split := event.text.split(" ", 1))) == 1:
                await event.edit("Reply to a plugin.")
                return
        path = split[1] + ".py"
        path = Path(__file__).parent / "plugins" /path
    Tamokuteki.load_plugin(path)
    await event.edit("Loaded plugin " + path)

@Tamokuteki.on(command(pattern = "unload "))
async def unloading(event):
    mod = event.text.split(" ", 1)[1]
    Tamokuteki.unload_plugin(mod)
    await event.edit("Unloaded plugin " + mod)

@Tamokuteki.on(command(pattern = "plugins"))
async def lplugins(event):
    plugins = Tamokuteki.list_plugins()
    msg = "Currently loaded plugins:\n\n"
    for plugin in plugins:
        msg += f"- `{plugin}`\n"
    await event.edit(msg)

__commands__ = {
    "load": "Load a plugin. Format: .load <plugin name>",
    "unload": "Unload a plugin. Format: .unload <plugin name>",
    "plugins": "List all loaded plugins.",
    "description": "[Core plugin]"
}
