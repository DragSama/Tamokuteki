from telethon import events

@Tamokuteki.on(events.NewMessage(pattern = ".start", outgoing  = True))
async def sup(event):
    await event.edit("Tamokuteki Bot V1")

__commands__ = {
    "start": "Check if bot is up and running."
}
