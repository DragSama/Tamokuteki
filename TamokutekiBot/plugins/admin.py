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

from TamokutekiBot.helpers import command


@Tamokuteki.command(pattern="purge")
async def purge(event):
    if not event.reply_to_msg_id:
        return
    split = event.text.split(" ", 1)
    if len(split) > 1 and split[1].isnumeric():
        purge_count = int(split[1])
    else:
        purge_count = None
    messages = []
    count = 0
    deleted = False
    async for message in Tamokuteki.iter_messages(
        event.chat_id, min_id=event.reply_to_msg_id, reverse=True
    ):
        if purge_count and count == purge_count:
            break
        count += 1
        if len(messages) == 100:
            await Tamokuteki.delete_messages(event.chat_id, messages)
            messages = []
            deleted = True
        else:
            messages.append(message)
            deleted = False
    if len(messages) <= 100:
        if not deleted:  # If message were not more than 100 so they never got deleted
            await Tamokuteki.delete_messages(event.chat_id, messages)
    await Tamokuteki.send_message(event.chat_id, f"Deleted {count} messages.")


@Tamokuteki.command(pattern=r"stats", outgoing=True)
async def get_stats(event):
    chat = event.text.split(" ", 1)[1]
    try:
        stats = await Tamokuteki.get_stats(chat)
    except:
        await event.reply(
            "Failed to get stats for the current chat, Make sure you are admin and chat has more than 500 members."
        )
        return
    min_time = stats.period.min_date.strftime("From %d/%m/%Y, %H:%M:%S")
    max_time = stats.period.max_date.strftime("To %d/%m/%Y, %H:%M:%S")
    member_count = int(stats.members.current) - int(stats.members.previous)
    message_count = int(stats.messages.current) - int(stats.messages.previous)
    msg = f"Group stats:\n{min_time} {max_time}\nMembers count increased by {member_count}\nMessage count increased by {message_count}"
    await event.reply(msg)


@Tamokuteki.command(pattern=r"(un)?pin", outgoing=True)
async def pin_message(event):
    message_id = event.reply_to_msg_id
    split = event.text.split(" ", 1)
    if len(split) > 1 and split[1] == "loud":
        is_loud = True
    else:
        is_loud = False
    await event.client.pin_message(event.chat_id, message_id, notify=is_loud)
    await event.edit("Done!")


@Tamokuteki.command(pattern=r"promote", outgoing=True)
async def promote(event):
    reply = await event.get_reply_message()
    if not reply:
        split = event.text.split(" ", 1)
        if len(split) == 1:
            await event.edit(
                "Reply to someone with .promote to promote them or .promote <username>"
            )
            return
        user = split[1]
    else:
        user = reply.sender_id
    split = event.text.split(" ")
    try:
        if len(split) > 1 and split[1] == "anonymous":
            await Tamokuteki.edit_admin(
                event.chat_id, user, is_admin=True, anonymous=True
            )
            await event.edit("Promoted as anonymous admin!")
        elif len(split) > 1:
            await Tamokuteki.edit_admin(
                event.chat_id, user, is_admin=True, title=split[1]
            )
            await event.edit(f"Promoted with custom title {split[1]}!")
        else:
            await Tamokuteki.edit_admin(
                event.chat_id, user, is_admin=True, anonymous=False
            )
            await event.edit("Promoted!")
    except Exception as e:
        await event.edit(str(e))
        return


@Tamokuteki.command(pattern=r"demote", outgoing=True)
async def demote(event):
    reply = await event.get_reply_message()
    if not reply:
        split = event.text.split(" ", 1)
        if len(split) == 1:
            await event.edit(
                "Reply to someone with .demote to demote them or use .demote <username>"
            )
            return
        user = split[1]
    else:
        user = reply.sender_id
    try:
        await Tamokuteki.edit_admin(event.chat_id, user, is_admin=False)
    except Exception as e:
        await event.edit(str(e))
        return
    await event.edit("Demoted!")


@Tamokuteki.command(pattern=r"ban", outgoing=True)
async def ban(event):
    reply = await event.get_reply_message()
    if not reply:
        split = event.text.split(" ", 1)
        if len(split) == 1:
            await event.edit(
                "Reply to someone with .ban to ban them from chat or use .ban <username>"
            )
            return
        user = split[1]
    else:
        user = reply.sender_id
    try:
        await Tamokuteki.edit_permissions(event.chat_id, user, view_messages=False)
    except Exception as e:
        await event.edit(str(e))
        return
    await event.edit("Banned!")


@Tamokuteki.command(pattern=r"kick", outgoing=True)
async def kick(event):
    reply = await event.get_reply_message()
    if not reply:
        split = event.text.split(" ", 1)
        if len(split) == 1:
            await event.edit(
                "Reply to someone with .kick to remove them from chat or use .kick <username>"
            )
            return
        user = split[1]
    else:
        user = reply.sender_id
    try:
        await Tamokuteki.kick_participant(event.chat_id, user)
    except Exception as e:
        await event.edit(str(e))
        return
    await event.edit("Kicked!")


@Tamokuteki.command(pattern=r"deadaccs", outgoing=True)
async def deadaccs_finder(event):
    count = 0
    split = event.text.split(" ", 1)
    if len(split) > 1 and split[1] == "kick":
        kick = True
    else:
        kick = False
    msg = await event.reply("Searching participants...")
    async for user in Tamokuteki.iter_participants(event.chat_id):
        if user.deleted:
            count += 1
            if kick:
                try:
                    await Tamokuteki.kick_participant(event.chat_id, user)
                except Exception as e:
                    await event.edit(
                        "Failed to kick deleted accounts, Make sure you are admin."
                    )
                    print(e)
                    await msg.delete()
                    return
    if not kick:
        await event.edit(f"Found {count} deleted accounts.")
    else:
        await event.edit(f"Kicked {count} deleted accounts.")
    await msg.delete()


__commands__ = {
    "stats": "Get group stats. Format: .stats <chat id or username>",
    "pin": "Pin a message in a group, Do without reply to unpin. Format: .pin <loud/None> // As reply (Optional)",
    "unpin": "Unpin a message. Format: .unpin",
    "purge": "Purge X messages from replied message. Format: .purge <count> // As reply",
    "promote": "Promote a user. Format: .promote <username or reply> // As reply (Optional)",
    "demote": "Demotes a user. Format: .demote <username or reply> // As reply (Optional)",
    "ban": "Bans a user. Format: .ban <username or reply> // As reply (Optional)",
    "kick": "Kick a user. Format: .kick <username or reply> // As reply (Optional)",
    "deadaccs": "Find deleted accounts. Format: .deadaccs <kick>",
}
