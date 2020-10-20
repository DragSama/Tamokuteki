from telethon import events

from pathlib import Path

@Tamokuteki.on(events.NewMessage(pattern = "\.load ", outgoing  = True))
async def loading(event):
    path = event.text.split(" ", 1)[1] + ".py"
    path = Path(__file__).parent / "plugins" /path
    Tamokuteki.load_plugin(path)
    await event.edit("Loaded plugin " + event.text.split(" ", 1)[1])

@Tamokuteki.on(events.NewMessage(pattern = "\.unload ", outgoing  = True))
async def unloading(event):
    mod = event.text.split(" ", 1)[1]
    Tamokuteki.unload_plugin(mod)
    await event.edit("Unloaded plugin " + mod)

@Tamokuteki.on(events.NewMessage(pattern = "\.plugins", outgoing  = True))
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
