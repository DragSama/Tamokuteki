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
    u = int(split[1]) if split[1].isnumeric() else split[1]
    if len(split) != 3:
        await event.edit('Format: .getrep <username or id> <message to send>')
        return
    try:
        async with event.client.conversation(u, timeout = 900) as conv:
            await conv.send_message(split[2])
            start_time = time.time()
            r = await conv.get_response()
            end_time = time.time()
            chat = await conv.get_chat()
            await r.forward_to(event.chat_id)
            msg = f"**Sent**:\n`{split[2]}`\n**To**: `{chat.first_name}`\nGot response in {round(end_time - start_time, 2)}s"
        await event.edit(msg)
    except ValueError as ve:
        await event.edit(f'Error:\n{ve}')
    except asyncio.exceptions.TimeoutError:
        await event.edit(f'Timeout, Failed to get reply from {u} within given timeout')

__commands__ = {
    "config": "Get repo.",
    "alive": "Check if userbot is running.",
    "getrep": "Send a message and wait for reply. Format: .getrep <username or id> <message to send>"
}
