from telethon import events
import re

def command(pattern, outgoing = True):
    return events.NewMessage(pattern = re.compile(f"^\.{pattern}$"), outgoing = outgoing)
