from TamokutekiBot.helpers import command


@Tamokuteki.on(command(pattern="alive", outgoing=True))
async def alive(event):
    await event.edit("I'm alive!")

@Tamokuteki.on(command(pattern="repo", outgoing=True))
async def repo(event):
    await event.edit("Tamokuteki Bot\nRepo: https://github.com/DragSama/Tamokuteki")

__commands__ = {
    "config": "Get repo.",
    "alive": "Check if userbot is running."
}
