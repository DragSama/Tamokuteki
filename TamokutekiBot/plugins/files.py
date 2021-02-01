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

from TamokutekiBot.helpers import command, format_bytes
import time
import asyncio

async def progress_message(current, total, _type, message, s) -> None:
    if time.time() - s % 10 == 0:
        total_size, total_type = format_bytes(total)
        curr_size, curr_type = format_bytes(total)
        await message.edit(f"{_type} {round(total_size, 2)} {total_type} out of {round(curr_size, 2)} {curr_type}")

@Tamokuteki.on(command(pattern="download"))
async def download_file(event) -> None:
    if not event.is_reply:
        await event.send("Format: .download <As reply>")
        return
    reply = await event.get_reply_message()
    message = await event.reply('Downloading...') # Not editing current message because if you edit current message with same content it will raise error while for this message it won't
    try:
        s = time.time()
        path = await Tamokuteki.download_media(
            reply,
            "Downloads/",
            progress_callback=lambda current, total: asyncio.get_event_loop().create_task(
                progress_message(current, total, 'Downloaded', message, s)
            )
        )
    except Exception as e:
        await event.send(f"An error occurred:\n{str(e)}")
        return
    await event.send(f"Successfully downloaded to {path}")


@Tamokuteki.on(command(pattern="upload"))
async def upload_file(event) -> None:
    split = event.text.split(" ", 1)
    if len(split) == 1:
        await event.send("Format: .upload location")
        return
    location = split[1]
    message = await event.reply('Uploading..') # Not editing current message because if you edit current message with same content it will raise error while for this message it won't
    try:
        s = time.time()
        await Tamokuteki.send_file(
            entity=event.chat_id,
            file=location,
            force_document=True,
            progress_callback=lambda current, total: asyncio.get_event_loop().create_task(
                progress_message(current, total, 'Uploaded', message, s)
            )
        )
    except Exception as e:
        await event.send(f"An error occurred:\n{str(e)}")
        return
    await event.send("Done!")


__commands__ = {
    "download": "Download a file. <As reply>",
    "upload": "Upload a file to telegram. Format: .upload <file location/url/file id>",
}
