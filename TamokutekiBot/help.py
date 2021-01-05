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


@Tamokuteki.on(command(pattern="help"))
async def help(event) -> None:
    plugins = Tamokuteki.list_plugins()
    split = event.text.split(" ", 1)
    if len(split) == 1:
        plugin = "help"
    else:
        plugin = split[1]
    command = None
    if "/" in plugin:
        plugin, command = plugin.split("/")
    if plugin not in plugins:
        await event.edit("Plugin is not loaded or doesn't exist.")
        return
    mod = Tamokuteki.get_plugin(plugin)
    if not hasattr(mod, "__commands__"):
        await event.edit("Help is not available for this plugin.")
        return
    commands = mod.__commands__
    if command:
        if command.lower() in commands:
            await event.edit(
                f"Help for `{command}` command of **{plugin.capitalize()}**:\n\n`{commands[command]}`"
            )
            return
    msg = f"Help for **{plugin.capitalize()}**:\n\n"
    for x in commands.keys():
        if x == "description":  # Add description at end of message not at random
            continue
        msg += f"**{x}**: `{commands[x]}`\n"
    description = commands.get("description", False)
    if description:
        msg += f"\n{description}"
    await event.edit(msg)


__commands__ = {
    "help": "Get help for plugin. Format: .help <plugin name>",
    "description": "[Core plugin]",
}
