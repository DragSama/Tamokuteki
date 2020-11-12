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

from TamokutekiBot.helpers import command

anime_search_query = """
query ($id: Int, $search: String) {
  Media(id: $id, type: ANIME, search: $search) {
    id
    title {
      romaji
      english
      native
    }
    description
    startDate {
      year
    }
    episodes
    season
    type
    format
    status
    duration
    studios {
      nodes {
        name
      }
    }
    trailer {
      id
      site
      thumbnail
    }
    averageScore
    genres
    bannerImage
  }
}
"""
def shorten(description):
    msg = ""
    if len(description) > 700:
        description = description[0:500] + '....'
        msg += f"\n`{description}`"
    else:
        msg += f"\n`{description}`"
    return msg

url = 'https://graphql.anilist.co'

@Tamokuteki.on(command(pattern = "anime", outgoing  = True))
async def anime(event):
    search = event.text.split(' ', 1)
    if len(search) == 1:
        await event.edit("Format: .anime <anime name>")
        return
    else:
        search = search[1]
    variables = {'search': search}
    json = await (await session.post(
        url,
        json={
            'query': anime_search_query,
            'variables': variables
            }
        )).json()
    if 'errors' in json.keys():
        await event.edit('No result found :(')
        return
    json = json['data'].get(
        'Media',
        None)
    if json:
        msg = f"**{json['title']['romaji']}**(`{json['title']['native']}`)\n**Type**: {(json['format'])}\n**Status**: {json['status']}\n**Episodes**: {json.get('episodes', 'N/A')}\n**Duration**: {json.get('duration', 'N/A')} Per Ep.\n**Score**: {json['averageScore']}"
        if json['genres']:
            msg += "\n**Genres**: `"
            for x in json['genres']:
                msg += f"{x}, "
        else:
            msg += "\n**Genres**: N/A"
        msg = msg[:-2] + '`\n'
        if json['studios']['nodes']:
            msg += "**Studios**: `"
            for x in json['studios']['nodes']:
                msg += f"{(x['name'])}, "
            msg = msg[:-2] + '`\n'
        info = json.get('siteUrl')
        stat_image = f"https://img.anili.st/media/{json['id']}"
        image = json.get('bannerImage', None)
        trailer = json.get('trailer', None)
        anime_id = json['id']
        if trailer:
            trailer_id = trailer.get('id', None)
            site = trailer.get('site', None)
            if site == "youtube":
                trailer = 'https://youtu.be/' + trailer_id
        description = json.get('description', 'N/A').replace(
            '<i>', '').replace(
            '</i>', '').replace(
            '<br>', '')
        msg += shorten(description)
        msg += f"[\u200c]({stat_image})"
        await Tamokuteki.send_message(event.chat_id, msg)

__commands__ = {
    "anime": "Search anime on AniList. Format: .anime <anime>"
}
