# Copyright (C) 2020 DragSama. All rights reserved. Source code available under the AGPL.
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


@Tamokuteki.on(command(pattern="download"))
async def download_file(event):
    if not event.is_reply:
        await event.edit("Format: .download <As reply>")
        return
    reply = await event.get_reply_message()
    try:
        path = await Tamokuteki.download_media(
            reply,
            "Downloads/",
            progress_callback=lambda current, total: event.edit(
                f"Downloaded {format_bytes(current)} out of {format_bytes(total)} "
            ),
        )
    except Exception as e:
        await event.edit(f"An error occurred:\n{str(e)}")
        return
    await event.edit(f"Successfully downloaded to {path}")


@Tamokuteki.on(command(pattern="upload"))
async def upload_file(event):
    split = event.text.split(" ", 1)
    if len(split) == 1:
        await event.edit("Format: .upload location")
        return
    location = split[1]
    try:
        await Tamokuteki.send_file(
            entity=event.chat_id,
            file=location,
            force_document=True,
            progress_callback=lambda current, total: event.edit(
                f"Uploaded {str(x) + ' ' for x in format_bytes(current)}out of {str(x) + ' ' for x in format_bytes(total)}"
            ),
        )
    except Exception as e:
        await event.edit(f"An error occurred:\n{str(e)}")
        return
    await event.edit("Done!")


__commands__ = {
    "download": "Download a file. <As reply>",
    "upload": "Upload a file to telegram. Format: .upload <file location/url/file id>",
}
