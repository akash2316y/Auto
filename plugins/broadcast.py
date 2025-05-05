from bot import Bot
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, PeerIdInvalid, InputUserDeactivated
import asyncio
import re
from config import ADMIN
from .db import tb
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
import asyncio

def parse_button_markup(text: str):
    lines = text.split("\n")
    buttons = []
    final_text_lines = []

    for line in lines:
        match = re.fullmatch(r"\[(.+?)\]\((https?://[^\s]+)\)", line.strip())
        if match:
            buttons.append([InlineKeyboardButton(match[1], url=match[2])])
        else:
            final_text_lines.append(line)

    return InlineKeyboardMarkup(buttons) if buttons else None, "\n".join(final_text_lines).strip()


@Client.on_message(filters.command("broadcast") & filters.private & filters.user(ADMIN))
async def broadcasting_func(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("<b>Reply to a message to broadcast.</b>")

    msg = await message.reply_text("Processing broadcast...")
    to_copy_msg = message.reply_to_message
    users_list = await tb.get_all_users()

    completed = 0
    failed = 0

    raw_text = to_copy_msg.caption or to_copy_msg.text or ""
    reply_markup, cleaned_text = parse_button_markup(raw_text)

    for i, user in enumerate(users_list):
        user_id = user.get("user_id")
        if not user_id:
            continue
        try:
            if to_copy_msg.text:
                await client.send_message(user_id, cleaned_text, reply_markup=reply_markup)
            elif to_copy_msg.photo:
                await client.send_photo(user_id, to_copy_msg.photo.file_id, caption=cleaned_text, reply_markup=reply_markup)
            elif to_copy_msg.video:
                await client.send_video(user_id, to_copy_msg.video.file_id, caption=cleaned_text, reply_markup=reply_markup)
            elif to_copy_msg.document:
                await client.send_document(user_id, to_copy_msg.document.file_id, caption=cleaned_text, reply_markup=reply_markup)
            else:
                await to_copy_msg.copy(user_id)
            completed += 1
        except (UserIsBlocked, PeerIdInvalid, InputUserDeactivated):
            await tb.delete_user(user_id)
            failed += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await to_copy_msg.copy(user_id)
                completed += 1
            except:
                failed += 1
        except Exception as e:
            print(f"Broadcast to {user_id} failed: {e}")
            failed += 1

        await msg.edit(f"Total: {i + 1}\nCompleted: {completed}\nFailed: {failed}")
        await asyncio.sleep(0.1)

    await msg.edit(
        f"😶‍🌫 <b>Broadcast Completed</b>\n\n👥 Total Users: <code>{len(users_list)}</code>\n✅ Successful: <code>{completed}</code>\n🤯 Failed: <code>{failed}</code>",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎭 Close", callback_data="close")]])
    )


@Bot.on_message(filters.private & filters.command('dbroadcast') & filters.user(ADMIN))
async def delete_broadcast(client, message):
    if message.reply_to_message:
        try:
            duration = int(message.command[1])
        except (IndexError, ValueError):
            return await message.reply("<b>Usage:</b> <code>/dbroadcast {duration_in_seconds}</code>")

        users = await db.full_userbase()  # Adjust function if it's named differently
        total = successful = blocked = deleted = unsuccessful = 0

        pls_wait = await message.reply("Broadcast with auto-delete processing...")

        for user_id in users:
            try:
                sent_msg = await message.reply_to_message.copy(user_id)
                await asyncio.sleep(duration)
                await sent_msg.delete()
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                sent_msg = await message.reply_to_message.copy(user_id)
                await asyncio.sleep(duration)
                await sent_msg.delete()
                successful += 1
            except UserIsBlocked:
                await db.del_user(user_id)
                blocked += 1
            except InputUserDeactivated:
                await db.del_user(user_id)
                deleted += 1
            except:
                unsuccessful += 1
            total += 1

        await pls_wait.edit_text(
            f"<b>Broadcast Completed</b>\n\n"
            f"Total: <code>{total}</code>\n"
            f"Successful: <code>{successful}</code>\n"
            f"Blocked: <code>{blocked}</code>\n"
            f"Deleted: <code>{deleted}</code>\n"
            f"Failed: <code>{unsuccessful}</code>"
        )
    else:
        await message.reply("Please reply to a message with /dbroadcast {duration_in_seconds}.")
