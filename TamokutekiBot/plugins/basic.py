from telethon import events

@Tamokuteki.on(events.NewMessage(pattern = ".config", outgoing  = True))
async def sup(event):
    await event.edit("Tamokuteki Bot\nRepo: https://github.com/DragSama/Tamokuteki")

__commands__ = {
    "config": "Get repo."
}
