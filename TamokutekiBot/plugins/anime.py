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

import tracemoepy

from TamokutekiBot.helpers import command, format_bytes
from TamokutekiBot.plugins.graphql_queries import anime_search_query, manga_query

url = "https://graphql.anilist.co"

tracemoe = tracemoepy.async_trace.Async_Trace(session=Tamokuteki.aio_session)


@Tamokuteki.command(pattern="anime", outgoing=True)
async def anime(event):
    search = event.text.split(" ", 1)
    if len(search) == 1:
        await event.edit("Format: .anime <anime name>")
        return
    else:
        search = search[1]
    variables = {"search": search}
    json = await (
        await session.post(
            url, json={"query": anime_search_query, "variables": variables}
        )
    ).json()
    if "errors" in json.keys():
        await event.edit("No result found :(")
        return
    json = json["data"].get("Media", None)
    if json:
        msg = f"**{json['title']['romaji']}**(`{json['title']['native']}`)\n**Type**: {(json['format'])}\n**Status**: {json['status']}\n**Episodes**: {json.get('episodes', 'N/A')}\n**Duration**: {json.get('duration', 'N/A')} Per Ep.\n**Score**: {json['averageScore']}"
        if json["genres"]:
            msg += "\n**Genres**: `"
            for x in json["genres"]:
                msg += f"{x}, "
        else:
            msg += "\n**Genres**: N/A"
        msg = msg[:-2] + "`\n"
        if json["studios"]["nodes"]:
            msg += "**Studios**: `"
            for x in json["studios"]["nodes"]:
                msg += f"{(x['name'])}, "
            msg = msg[:-2] + "`\n"
        info = json.get("siteUrl")
        stat_image = f"https://img.anili.st/media/{json['id']}"
        image = json.get("bannerImage", None)
        trailer = json.get("trailer", None)
        anime_id = json["id"]
        if trailer:
            trailer_id = trailer.get("id", None)
            site = trailer.get("site", None)
            if site == "youtube":
                trailer = "https://youtu.be/" + trailer_id
        description = (
            json.get("description", "N/A")
            .replace("<i>", "")
            .replace("</i>", "")
            .replace("<br>", "")
        )
        msg += description
        msg += f"[\u200c]({stat_image})"
        await Tamokuteki.send_message(event.chat_id, msg)


@Tamokuteki.command(pattern="manga", outgoing=True)
async def manga(event):
    search = event.text.split(" ", 1)
    if len(search) == 1:
        update.effective_message.reply_text("Format : .manga < manga name >")
        return
    search = search[1]
    variables = {"search": search}
    json = requests.post(
        url, json={"query": manga_query, "variables": variables}
    ).json()
    msg = ""
    if "errors" in json.keys():
        update.effective_message.reply_text("Manga not found")
        return
    json = json["data"]
    if json:
        json = json["Media"]
        stat_image = f"https://img.anili.st/media/{json['id']}"
        title, title_native = json["title"].get("romaji", False), json["title"].get(
            "native", False
        )
        start_date, status, score = (
            json["startDate"].get("year", False),
            json.get("status", False),
            json.get("averageScore", False),
        )
        if title:
            msg += f"*{title}*"
            if title_native:
                msg += f"(`{title_native}`)"
        if start_date:
            msg += f"\n*Start Date* - `{start_date}`"
        if status:
            msg += f"\n*Status* - `{status}`"
        if score:
            msg += f"\n*Score* - `{score}`"
        msg += "\n*Genres* - "
        for x in json.get("genres", []):
            msg += f"{x}, "
        msg = msg[:-2]
        msg += f"_{json.get('description', 'description N/A')}_"
        msg += f"[\u200c]({stat_image})"
        await event.edit(msg)


@Tamokuteki.command(pattern="reverse", outgoing=True)
async def reverse(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    if not reply_message:
        await event.edit("Reply to a gif/video/image to reverse search.")
        return
    if reply_message.video or reply_message.gif:
        file = await Tamokuteki.download_media(
            reply_message,
            thumb=-1,
            progress_callback=lambda current, total: event.edit(
                f"Downloaded {format_bytes(current)} out of {format_bytes(total)} "
            ),
        )
    else:
        file = await Tamokuteki.download_media(
            reply_message,
            progress_callback=lambda current, total: event.edit(
                f"Downloaded {format_bytes(current)} out of {format_bytes(total)} "
            ),
        )
    search = await tracemoe.search(file, upload_file=True)
    result = search["docs"][0]
    msg = (
        f"**Title**: {result['title_english']}"
        f"\n**Similarity**: {result['similarity']*100}"
        f"\n**Episode**: {result['episode']}"
    )
    preview = await tracemoe.natural_preview(search)
    with open("preview.mp4", "wb") as f:
        f.write(preview)
    await event.edit(msg)
    await Tamokuteki.send_file(
        event.chat_id, "preview.mp4", caption="Match", force_document=False
    )


__commands__ = {
    "anime": "Search anime on AniList. Format: .anime <anime>",
    "manga": "Search manga on AniList. Format: .manga <manga>",
    "reverse": "Reverse search a image or video to find original anime. Format: .reverse <As reply>",
}
