from pyrogram import Client, filters, enums
from pyrogram.errors import *
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import *
import asyncio
from Script import text
from .db import tb
from .fsub import get_fsub

@Client.on_message(filters.command("start"))
async def start_cmd(client, message):
    if await tb.get_user(message.from_user.id) is None:
        await tb.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL,
            text.LOG.format(message.from_user.mention, message.from_user.id)
        )

    if IS_FSUB and not await get_fsub(client, message):
        return await message.reply_text(
            text.START.format(message.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('⇆ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs ⇆', url="https://t.me/AutoAcceptorXBot?startgroup=true&admin=invite_users")],
                [InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about'), InlineKeyboardButton('ʜᴇʟᴘ', callback_data='help')],
                [InlineKeyboardButton('⇆ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ⇆', url="https://t.me/AutoAcceptorXBot?startchannel=true&admin=invite_users")]
            ]),
            reply_to_message_id=message.id  # 👈 Yeh line ensure karta hai reply
        )

    await message.reply_text(
        text.START.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('⇆ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs ⇆', url="https://t.me/AutoAcceptorXBot?startgroup=true&admin=invite_users")],
            [InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about'), InlineKeyboardButton('ʜᴇʟᴘ', callback_data='help')],
            [InlineKeyboardButton('⇆ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ⇆', url="https://t.me/AutoAcceptorXBot?startchannel=true&admin=invite_users")]
        ]),
        reply_to_message_id=message.id  # 👈 Yeh line bhi add karo
    )

@Client.on_message(filters.command("stats") & filters.private & filters.user(ADMIN))
async def total_users(client, message):
    try:
        users = await tb.get_all_users()
        await message.reply(f"👥 **Total Users:** {len(users)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎭 Close", callback_data="close")]]))
    except Exception as e:
        r = await message.reply(f"❌ *Error:* `{str(e)}`")
        await asyncio.sleep(30)
        await r.delete()

@Client.on_message(filters.command('accept') & filters.private)
async def accept(client, message):
    show = await message.reply("𝖯𝗅𝖾𝖺𝗌𝖾 𝖶𝖺𝗂𝗍.....")
    user_data = await tb.get_session(message.from_user.id)
    if user_data is None:
        return await show.edit("𝖥𝗈𝗋 𝖠𝖼𝖼𝖾𝗉𝗍 𝖯𝖾𝗇𝖽𝗂𝗇𝗀 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝖸𝗈𝗎 𝖧𝖺𝗏𝖾 𝖳𝗈 /login 𝖥𝗂𝗋𝗌𝗍.")

    try:
        acc = Client("joinrequest", session_string=user_data, api_id=API_ID, api_hash=API_HASH)
        await acc.connect()
    except:
        return await show.edit("𝖸𝗈𝗎𝗋 𝖫𝗈𝗀𝗂𝗇 𝖲𝖾𝗌𝗌𝗂𝗈𝗇 𝖤𝗑𝗉𝗂𝗋𝖾𝖽. 𝖲𝗈 /logout  𝖥𝗂𝗋𝗌𝗍 𝖳𝗁𝖾𝗇 𝖫𝗈𝗀𝗂𝗇 𝖠𝗀𝖺𝗂𝗇 𝖡𝗒 - /login")

    await show.edit("𝖭𝗈𝗐 𝖥𝗈𝗋𝗐𝖺𝗋𝖽 𝖠 𝖬𝖾𝗌𝗌𝖺𝗀𝖾 𝖥𝗋𝗈𝗆 𝖸𝗈𝗎𝗋 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖮𝗋 𝖦𝗋𝗈𝗎𝗉 𝖶𝗂𝗍𝗁 𝖥𝗈𝗋𝗐𝖺𝗋𝖽 𝖳𝖺𝗀\n\n𝖬𝖺𝗄𝖾 𝖲𝗎𝗋𝖾 𝖸𝗈𝗎𝗋 𝖫𝗈𝗀𝗀𝖾𝖽 𝖨𝗇 𝖠𝖼𝖼𝗈𝗎𝗇𝗍 𝖨𝗌 𝖠𝖽𝗆𝗂𝗇 𝖨𝗇 𝖳𝗁𝖺𝗍 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖮𝗋 𝖦𝗋𝗈𝗎𝗉 𝖶𝗂𝗍𝗁 𝖥𝗎𝗅𝗅 𝖱𝗂𝗀𝗁𝗍𝗌..")
    fwd_msg = await client.listen(message.chat.id)

    if fwd_msg.forward_from_chat and fwd_msg.forward_from_chat.type not in [enums.ChatType.PRIVATE, enums.ChatType.BOT]:
        chat_id = fwd_msg.forward_from_chat.id
        try:
            info = await acc.get_chat(chat_id)
        except:
            return await show.edit("𝖤𝗋𝗋𝗈𝗋 - 𝖬𝖺𝗄𝖾 𝖲𝗎𝗋𝖾 𝖸𝗈𝗎𝗋 𝖫𝗈𝗀𝗀𝖾𝖽 𝖨𝗇 𝖠𝖼𝖼𝗈𝗎𝗇𝗍 𝖨𝗌 𝖠𝖽𝗆𝗂𝗇 𝖨𝗇 𝖳𝗁𝗂𝗌 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖮𝗋 𝖦𝗋𝗈𝗎𝗉 𝖶𝗂𝗍𝗁 𝖱𝗂𝗀𝗁𝗍𝗌.")
    else:
        return await message.reply("𝖬𝖾𝗌𝗌𝖺𝗀𝖾 𝖭𝗈𝗍 𝖥𝗈𝗋𝗐𝖺𝗋𝖽𝖾𝖽 𝖥𝗋𝗈𝗆 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖮𝗋 𝖦𝗋𝗈𝗎𝗉.*")

    await fwd_msg.delete()
    msg = await show.edit("𝖠𝖼𝖼𝖾𝗉𝗍𝗂𝗇𝗀 𝖺𝗅𝗅 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍𝗌... 𝖯𝗅𝖾𝖺𝗌𝖾 𝗐𝖺𝗂𝗍 𝗎𝗇𝗍𝗂𝗅 𝗂𝗍'𝗌 𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽.")
    try:
        while True:
            await acc.approve_all_chat_join_requests(chat_id)
            await asyncio.sleep(1)
            join_requests = [req async for req in acc.get_chat_join_requests(chat_id)]
            if not join_requests:
                break
        await msg.edit("𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖺𝖼𝖼𝖾𝗉𝗍𝖾𝖽 𝖺𝗅𝗅 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍𝗌.")
    except Exception as e:
        await msg.edit(f"**An error occurred:** `{str(e)}`")


@Client.on_chat_join_request()
async def approve_new(client, m):
    if not NEW_REQ_MODE:
        return
    try:
        await client.approve_chat_join_request(m.chat.id, m.from_user.id)
        try:
            await client.send_message(
                m.from_user.id,
                f"𝖧𝖾𝗒 {m.from_user.mention},\n\n𝖸𝗈𝗎𝗋 𝖱𝖾𝗊𝗎𝗌𝗍 𝖳𝗈 𝖩𝗈𝗂𝗇 {m.chat.title} 𝖧𝖺𝗌 𝖡𝖾𝖾𝗇 𝖠𝖼𝖼𝖾𝗉𝗍𝖾𝖽."
            )
        except:
            pass
    except Exception as e:
        print(str(e))
        pass
