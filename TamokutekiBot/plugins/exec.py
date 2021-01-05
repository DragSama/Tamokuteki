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

from telethon import events

from io import StringIO
import traceback
import sys

# Thanks to stackoverflow for existing https://stackoverflow.com/questions/3906232/python-get-the-print-output-in-an-exec-statement


@Tamokuteki.on(events.NewMessage(pattern="\.eval", outgoing=True))
async def evaluate(event):
    split = event.text.split(" ", 1)
    if len(split) == 1:
        await event.edit("Format: .eval <command>")
        return
    try:
        evaluation = eval(split[1])
    except Exception as e:
        evaluation = e
    await event.edit(str(evaluation))


@Tamokuteki.on(events.NewMessage(pattern="\.exec", outgoing=True))
async def execute(event):
    split = event.text.split(" ", 1)
    if len(split) == 1:
        await event.edit("Format: .exec <command>")
        return
    stderr, output, wizardry = None, None, None
    code = split[1]
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    try:
        await async_exec(code, event)
    except Exception:
        wizardry = traceback.format_exc()
    output = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    final = f"Command:\n`{code}`\n"
    sys.stderr = old_stderr
    if wizardry:
        final += "**Output**:\n`" + wizardry
    elif output:
        final += "**Output**:\n`" + output
    elif stderr:
        final += "**Output**:\n`" + stderr
    else:
        final = "`OwO no output"
    if len(final) >= 4096:
        with open("output.txt", "w+") as file:
            file.write(final)
        await Tamokuteki.send_file(event.chat_id, "output.txt", caption=code)
        return
    await event.edit(final + "`")


async def async_exec(code, event):
    exec(
        f"async def __async_exec(event): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__async_exec"](event)


__commands__ = {"exec": "Execute code.", "eval": "Evaluate code."}
