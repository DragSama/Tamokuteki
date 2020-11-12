from TamokutekiBot.helpers import command


@Tamokuteki.on(command(pattern="config", outgoing=True))
async def config(event):
    await event.edit("Tamokuteki Bot\nRepo: https://github.com/DragSama/Tamokuteki")

__commands__ = {
    "config": "Get repo."
}
