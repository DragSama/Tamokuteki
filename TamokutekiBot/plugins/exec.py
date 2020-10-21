from telethon import events

from TamokutekiBot.core import command

from io import StringIO
import traceback
import sys

#Thanks to stackoverflow for existing https://stackoverflow.com/questions/3906232/python-get-the-print-output-in-an-exec-statement

@Tamokuteki.on(command(pattern = "\.eval", outgoing  = True))
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

@Tamokuteki.on(command(pattern = "\.exec", outgoing  = True))
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
    sys.stderr = old_stderr
    if wizardry: final = "**Output**:\n`" + wizardry
    elif output: final = "**Output**:\n`" + output
    elif stderr: final = "**Output**:\n`" + stderr
    else: final = "`OwO no output"
    await event.edit(final + '`' )

async def async_exec(code, event):
    exec(
        f'async def __async_exec(event): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__async_exec'](event)

__commands__ = {
    "exec": "Execute code.",
    "eval": "Evaluate code."
}
