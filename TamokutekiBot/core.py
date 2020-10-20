from telethon import events

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
    "unload": "Unload a plugin. Format: .unload <plugin name>",
    "plugins": "List all loaded plugins.",
    "description": "[Core plugin]"
}
