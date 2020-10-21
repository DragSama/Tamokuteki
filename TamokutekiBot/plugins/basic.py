from telethon import events
from TamokutekiBot.core import command

@Tamokuteki.on(command(pattern = ".config", outgoing  = True))
async def sup(event):
    await event.edit("Tamokuteki Bot\nRepo: https://github.com/DragSama/Tamokuteki")

__commands__ = {
    "config": "Get repo."
}
