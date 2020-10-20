from telethon import events

@Tamokuteki.on(events.NewMessage(pattern = "\.help", outgoing  = True))
async def help(event) -> None:
    plugins = Tamokuteki.list_plugins()
    split = event.text.split(" ", 1)
    if len(split) == 1:
        plugin = "help"
    else:
        plugin = split[1]
    if plugin not in plugins:
        await event.edit("Plugin is not loaded or doesn't exist.")
        return
    mod = Tamokuteki.get_plugin(plugin)
    if not hasattr(mod, "__commands__"):
        await event.edit("Help is not available for this plugin.")
        return
    msg = f"Help for **{plugin.capitalize()}**:\n\n"
    commands = mod.__commands__
    for x in commands.keys():
        if x == "description": # Add description at end of message not at random
            continue
        msg += f"**{x}**: `{commands[x]}`\n"
    description = commands.get("description", False)
    if description:
        msg += f"\n{description}"
    await event.edit(msg)

__commands__ = {
    "help": "Get help for plugin. Format: .help <plugin name>",
    "description": "[Core plugin]"
}
