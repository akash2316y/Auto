import traceback
from pyrogram.types import Message
from pyrogram import Client, filters
from asyncio.exceptions import TimeoutError
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from config import *
from .db import tb

SESSION_STRING_SIZE = 351

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["logout"]))
async def logout(client, message):
    user_id = message.from_user.id
    session = await tb.get_session(user_id)
    if session is None:
        return
    await tb.set_session(user_id, session=None)
    await message.reply("**Logout Successfully** ♦")

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["login"]))
async def main(bot: Client, message: Message):
    user_id = message.from_user.id
    session = await tb.get_session(user_id)
    if session is not None:
        await message.reply("**You are already logged in. Please /logout first before logging in again.**")
        return

    # Ask for phone number
    phone_number_msg = await bot.ask(
        chat_id=user_id,
        text="<b>Please send your phone number which includes country code</b>\n<b>Example:</b> <code>+13124562345, +9171828181889</code>"
    )
    if phone_number_msg.text == '/cancel':
        return await phone_number_msg.reply('<b>Process cancelled!</b>')

    phone_number = phone_number_msg.text
    client = Client(":memory:", API_ID, API_HASH)
    await client.connect()
    await phone_number_msg.reply("Sending OTP...")

    try:
        code = await client.send_code(phone_number)
        phone_code_msg = await bot.ask(
            user_id,
            "Check your official Telegram account for OTP. If you got it, send it here as shown:\n\nIf OTP is `12345`, **send as** `1 2 3 4 5`.\n\n**Enter /cancel to cancel.**",
            filters=filters.text,
            timeout=600
        )
    except PhoneNumberInvalid:
        return await phone_number_msg.reply('`PHONE_NUMBER` **is invalid.**')

    if phone_code_msg.text == '/cancel':
        return await phone_code_msg.reply('<b>Process cancelled!</b>')

    try:
        phone_code = phone_code_msg.text.replace(" ", "")
        await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except PhoneCodeInvalid:
        return await phone_code_msg.reply('**OTP is invalid.**')
    except PhoneCodeExpired:
        return await phone_code_msg.reply('**OTP is expired.**')
    except SessionPasswordNeeded:
        two_step_msg = await bot.ask(
            user_id,
            '𝖳𝗐𝗈-𝗌𝗍𝖾𝗉 𝗏𝖾𝗋𝗂𝖿𝗂𝖼𝖺𝗍𝗂𝗈𝗇 𝗂𝗌 𝖾𝗇𝖺𝖻𝗅𝖾𝖽. 𝖯𝗅𝖾𝖺𝗌𝖾 𝗌𝖾𝗇𝖽 𝗒𝗈𝗎𝗋 𝗉𝖺𝗌𝗌𝗐𝗈𝗋𝖽.\𝗇\𝗇𝖤𝗇𝗍𝖾𝗋 /cancel 𝗍𝗈 𝖼𝖺𝗇𝖼𝖾𝗅.',
            filters=filters.text,
            timeout=300
        )
        if two_step_msg.text == '/cancel':
            return await two_step_msg.reply('𝖯𝗋𝗈𝖼𝖾𝗌𝗌 𝖼𝖺𝗇𝖼𝖾𝗅𝗅𝖾𝖽!')
        try:
            await client.check_password(password=two_step_msg.text)
        except PasswordHashInvalid:
            return await two_step_msg.reply('𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝗉𝖺𝗌𝗌𝗐𝗈𝗋𝖽 𝗉𝗋𝗈𝗏𝗂𝖽𝖾𝖽')

    # Generate session string
    string_session = await client.export_session_string()
    await client.disconnect()

    if len(string_session) < SESSION_STRING_SIZE:
        return await message.reply('𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝗌𝖾𝗌𝗌𝗂𝗈𝗇 𝗌𝗍𝗋𝗂𝗇𝗀')

    try:
        # Store in database
        await tb.set_session(user_id, string_session)
    except Exception as e:
        return await message.reply_text(f"𝖤𝖱𝖱𝖮𝖱 𝖨𝖭 𝖫𝖮𝖦𝖨𝖭: `{e}`")

    await bot.send_message(
        user_id,
        "𝖠𝖼𝖼𝗈𝗎𝗇𝗍 𝗅𝗈𝗀𝗀𝖾𝖽 𝗂𝗇 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒.\𝗇\𝗇𝖨𝖿 𝗒𝗈𝗎 𝗀𝖾𝗍 𝖺𝗇𝗒 𝖠𝖴𝖳𝖧 𝖪𝖤𝖸 𝗋𝖾𝗅𝖺𝗍𝖾𝖽 𝖾𝗋𝗋𝗈𝗋, 𝗎𝗌𝖾 /logout 𝖺𝗇𝖽 /login 𝖺𝗀𝖺𝗂𝗇."
    )
