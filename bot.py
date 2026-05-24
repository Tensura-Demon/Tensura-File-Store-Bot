from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from pyrogram.types import InputMediaPhoto
from pyrogram.enums import ParseMode
import os
import sys
import random
import psutil

IMAGES = [
    "https://graph.org/file/98245197c3a4185b49dbe-3df65fb012e4195cff.jpg",
    "https://graph.org/file/27dd5451f160ce28dadd4-8ca0a7d6480451adc8.jpg",
    "https://graph.org/file/0e77ba48a8b7a3b09296f-362372bee0d84fd217.jpg"
]
from database import (
    save_file, get_file, add_user, get_all_users, total_users,
    add_admin_db, remove_admin_db, is_admin, get_all_admins
)

from keep_alive import keep_alive
import asyncio
import time

START_TIME = time.time()
BOT_VERSION = "v3.0"

app = Client(
    "filelinkbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

import re
import base64

# helper function
async def get_message_id(client, message: Message):
    try:
        if not message.text:
            return None, None

        link = message.text.strip()

        # private channel
        if "/c/" in link:
            parts = link.split("/")
            chat_id = int("-100" + parts[-2])
            msg_id = int(parts[-1])
            return msg_id, chat_id

        # public channel
        match = re.search(r"t\.me/([^/]+)/(\d+)", link)

        if match:
            username = match.group(1)
            msg_id = int(match.group(2))

            chat = await client.get_chat(username)

            return msg_id, chat.id

        return None, None

    except:
        return None, None


#batch

BATCH_USERS = {}

#Only Owner + Admin Can Generate Batch Links
# ================= BATCH COMMAND =================

@app.on_message(filters.private & filters.command("batch"))
async def batch(client, message: Message):

    user_id = message.from_user.id

    # ONLY OWNER + ADMINS
    if user_id != OWNER_ID and not await is_admin(user_id):
        return await message.reply_text(
            "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ᴍᴀsᴛᴇʀ. ɢᴏ ᴀᴡᴀʏ, ʙɪᴛᴄʜ 🙃..."
        )

    BATCH_USERS[user_id] = {
        "step": "first"
    }

    await message.reply_text(
        "Gɪᴠᴇ Mᴇ Bᴀᴛᴄʜ Fɪʀsᴛ Mᴇssᴀɢᴇ 𝗟𝗶𝗻𝗸 ғʀᴏᴍ ʏᴏᴜʀ 𝗗𝗕 𝗖𝗵𝗮𝗻𝗻𝗲𝗹"
    )

# ================= HANDLE BATCH REPLIES =================

@app.on_message(filters.private & filters.text)
async def handle_batch(client, message: Message):

    user_id = message.from_user.id

    if user_id not in BATCH_USERS:
        return

    data = BATCH_USERS[user_id]

    # FIRST LINK
    if data["step"] == "first":

        f_msg_id, chat_id = await get_message_id(client, message)

        if not f_msg_id:
            return await message.reply_text("‼️ Iɴᴠᴀʟɪᴅ Lᴀsᴛ Mᴇssᴀɢᴇ Lɪɴᴋ")

        data["first"] = f_msg_id
        data["chat_id"] = chat_id
        data["step"] = "last"

        return await message.reply_text("Gɪᴠᴇ Mᴇ Bᴀᴛᴄʜ Lᴀsᴛ Mᴇssᴀɢᴇ 𝗟𝗶𝗻𝗸 ғʀᴏᴍ ʏᴏᴜʀ 𝗗𝗕 𝗖𝗵𝗮𝗻𝗻𝗲𝗹")

    # LAST LINK
    elif data["step"] == "last":

        l_msg_id, _ = await get_message_id(client, message)

        if not l_msg_id:
            return await message.reply_text("‼️ Iɴᴠᴀʟɪᴅ Lᴀsᴛ Mᴇssᴀɢᴇ Lɪɴᴋ")

        f_msg_id = data["first"]

        if l_msg_id <= f_msg_id:
            return await message.reply_text(
                "‼️ Lᴀsᴛ ᴍᴇssᴀɢᴇ ᴍᴜsᴛ ʙᴇ ɢʀᴇᴀᴛᴇʀ ᴛʜᴀɴ ғɪʀsᴛ"
            )

        # ENCODE
        string = f"get-{f_msg_id}-{l_msg_id}"

        base64_string = base64.urlsafe_b64encode(
            string.encode()
        ).decode().strip("=")

        bot_username = (await client.get_me()).username

        link = f"https://t.me/{bot_username}?start={base64_string}"

        await message.reply_text(
            f"✅ ʙᴀᴛᴄʜ ʟɪɴᴋs ɢᴇɴᴇʀᴀᴛᴇᴅ\n\n`{link}`",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔗 sʜᴀʀᴇ ʟɪɴᴋ",
                        url=f"https://telegram.me/share/url?url={link}"
                    )
                ]
            ])
        )

        del BATCH_USERS[user_id]

# START + LINK HANDLER
@app.on_message(filters.command("start"))
async def start(client, message: Message):
    
    user_id = message.from_user.id
    
    await add_user(message.from_user.id)

    # START ANIMATION
    m = await message.reply_text("ᴍᴏɴᴋᴇʏ ᴅ ʟᴜғғʏ\nɢᴇᴀʀ 𝟻. . .")
    await asyncio.sleep(0.5)
    await m.edit_text("🎊")
    await asyncio.sleep(0.5)
    await m.edit_text("⚡")
    await asyncio.sleep(0.5)
    await m.edit_text("sᴜɴ ɢᴏᴅ ɴɪᴋᴀ!...")
    await asyncio.sleep(0.5)
    await m.delete()

    await message.reply_sticker("CAACAgUAAxkBAAEXmw5plIsM5lyaJfj5NwNp13QSrbW9NQACnBsAAlztqVYRMk2x1suA_B4E")

    if len(message.command) > 1:

    param = message.command[1]

    else:

         photo = random.choice(IMAGES)

         return await message.reply_photo(
             photo=photo,
             caption=(
                 "𝗛𝗲𝗹𝗹𝗼 ♡,\n\n"
                 "›› 𝗜 𝗰𝗮𝗻 𝘀𝘁𝗼𝗿𝗲 𝗽𝗿𝗶𝘃𝗮𝘁𝗲 𝗳𝗶𝗹𝗲𝘀 𝗶𝗻 𝗦𝗽𝗲𝗰𝗶𝗳𝗶𝗲𝗱 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗮𝗻𝗱 𝗼𝘁𝗵𝗲𝗿 𝘂𝘀𝗲𝗿𝘀 𝗰𝗮𝗻 𝗮𝗰𝗰𝘀𝘀 𝗶𝘁 ғʀᴏᴍ sᴘᴇᴄɪᴀʟ ʟɪɴᴋ."
             ),
             reply_markup=InlineKeyboardMarkup(
                 [
                    [
                         InlineKeyboardButton(
                             "ᴜᴘᴅᴀᴛᴇs",
                              url="https://t.me/Anime_UpdatesAU"
                         ),
                         InlineKeyboardButton(
                             "ᴀʙᴏᴜᴛ",
                             callback_data="about"
                         )
                    ],
                    [
                         InlineKeyboardButton(
                             "ᴏᴡɴᴇʀ",
                             url="https://t.me/+ssaZDrj3Wr4wNzI1"
                         )
                    ]
                ]
             ),
             parse_mode=ParseMode.MARKDOWN
         )
        # ================= BATCH LINK =================

        try:

            decoded = base64.urlsafe_b64decode(
                param + "=" * (-len(param) % 4)
            ).decode()

            if decoded.startswith("get-"):

                _, first_id, last_id = decoded.split("-")

                first_id = int(first_id)
                last_id = int(last_id)

                x = await message.reply_text(
                    "🔗 ғɪʟᴇs ʟɪɴᴋs ɢᴇɴᴇʀᴀᴛᴇᴅ..."
                )

                await asyncio.sleep(0.5)

                await x.edit_text("✨️ ғɪʟᴇs ʟᴏᴀᴅɪɴɢ...")

                await asyncio.sleep(0.5)

                await x.edit_text("⏳️ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...")

                await asyncio.sleep(0.5)

                await x.delete()
                
                sent_msgs = []

                for msg_id in range(first_id, last_id + 1):

                    try:

                        msg = await client.get_messages(
                            CHANNEL_ID,
                            msg_id
                        )

                        original_caption = msg.caption if msg.caption else ""

                        caption = (
                            f"**{original_caption}**\n\n"
                            f"**›› Cʜᴀɴɴᴇʟ :** "
                            f"[ᴀɴɪᴍᴇ ᴜᴘᴅᴀᴛᴇs](https://t.me/Anime_UpdatesAU)"
                        )

                        buttons = InlineKeyboardMarkup(
                            [[
                                InlineKeyboardButton(
                                    "ᴜᴘᴅᴀᴛᴇs",
                                    url="https://t.me/Anime_UpdatesAU"
                                )
                            ]]
                        )

                        if msg.video:

                            sent = await message.reply_video(
                                msg.video.file_id,
                                caption=caption,
                                reply_markup=buttons,
                                supports_streaming=True,
                                parse_mode=ParseMode.MARKDOWN
                            )
                            
                            sent_msgs.append(sent)

                        elif msg.document:

                            sent = await message.reply_document(
                                msg.document.file_id,
                                caption=caption,
                                reply_markup=buttons,
                                parse_mode=ParseMode.MARKDOWN
                            )
                            
                            sent_msgs.append(sent)

                        elif msg.audio:

                            sent = await message.reply_audio(
                                msg.audio.file_id,
                                caption=caption,
                                reply_markup=buttons,
                                parse_mode=ParseMode.MARKDOWN
                            )
                            
                            sent_msgs.append(sent)

                        elif msg.animation:

                            sent = await message.reply_animation(
                                msg.animation.file_id,
                                caption=caption,
                                reply_markup=buttons,
                                parse_mode=ParseMode.MARKDOWN
                            )
                            
                            sent_msgs.append(sent)

                        elif msg.sticker:

                            sent = await message.reply_sticker(
                                msg.sticker.file_id
                            )
                            
                            sent_msgs.append(sent)

                        await asyncio.sleep(0.3)

                    except Exception as e:
                        print(e)

                warn = await message.reply_text(
                    " ⏳ Dᴜᴇ ᴛᴏ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs...\n\n"
                    " ›› Yᴏᴜʀ ғɪʟᴇs ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ᴡɪᴛʜɪɴ 𝟻 ᴍɪɴᴜᴛᴇs.\n"
                    " ›› Sᴏ ᴘʟᴇᴀsᴇ ғᴏʀᴡᴀʀᴅ ᴛʜᴇᴍ ᴛᴏ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs.\n\n"
                    " ›› 𝗡𝗼𝘁𝗲: ᴜsᴇ 𝗩𝗟𝗖 𝗣𝗹𝗮𝘆𝗲𝗿 ᴏʀ 𝗠𝗫 𝗣𝗹𝗮𝘆𝗲𝗿 ғᴏʀ ʙᴇsᴛ ᴇxᴘᴇʀɪᴇɴᴄᴇ."
                )

                await asyncio.sleep(300)

                for msg in sent_msgs:
                    try:
                        await msg.delete()
                    except:
                        pass

                try:
                    await warn.delete()
                except:
                    pass

    # ================= SINGLE FILE =================

    file_unique_id = param

    data = await get_file(file_unique_id)

    if not data:
        return await message.reply_text(
            "🔎 Fɪʟᴇ Is Nᴏᴛ Fᴏᴜɴᴅ, Cᴏɴᴛᴀᴄᴛ Tᴏ Oᴡɴᴇʀ."
        )

    original_caption = data.get("caption", "")

    caption = (
        f"**{original_caption}**\n\n"
        f"**›› Cʜᴀɴɴᴇʟ :** "
        f"[ᴀɴɪᴍᴇ ᴜᴘᴅᴀᴛᴇs](https://t.me/Anime_UpdatesAU)"
    )

    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                "ᴜᴘᴅᴀᴛᴇs",
                url="https://t.me/Anime_UpdatesAU"
            )
        ]]
    )

    if data.get("file_type") == "video":

        sent = await message.reply_video(
            data["file_id"],
            caption=caption,
            reply_markup=buttons,
            thumb=data.get("thumb")
            if data.get("thumb") else None,
            supports_streaming=True,
            parse_mode=ParseMode.MARKDOWN
        )

    elif data.get("file_type") == "audio":

        sent = await message.reply_audio(
            data["file_id"],
            caption=caption,
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN
        )

    elif data.get("file_type") == "document":

        sent = await message.reply_document(
            data["file_id"],
            caption=caption,
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN
        )

    elif data.get("file_type") == "sticker":

        sent = await message.reply_sticker(
            data["file_id"]
        )

    elif data.get("file_type") == "animation":

        sent = await message.reply_animation(
            data["file_id"],
            caption=caption,
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN
        )

    else:
        return await message.reply_text(
            "‼️ ᴜɴsᴜᴘᴘᴏʀᴛᴇᴅ ғᴏʀᴍᴀᴛ"
        )

    warn = await message.reply_text(
        " ⏳ Dᴜᴇ ᴛᴏ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs...\n\n"
        " ›› Yᴏᴜʀ ғɪʟᴇs ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ᴡɪᴛʜɪɴ 𝟻 ᴍɪɴᴜᴛᴇs.\n"
        " ›› Sᴏ ᴘʟᴇᴀsᴇ ғᴏʀᴡᴀʀᴅ ᴛʜᴇᴍ ᴛᴏ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs.\n\n"
        " ›› 𝗡𝗼𝘁𝗲: ᴜsᴇ 𝗩𝗟𝗖 𝗣𝗹𝗮𝘆𝗲𝗿 ᴏʀ 𝗠𝗫 𝗣𝗹𝗮𝘆𝗲𝗿 ғᴏʀ ʙᴇsᴛ ᴇxᴘᴇʀɪᴇɴᴄᴇ."
    )

    # AFTER FILE ANIMATION
    m2 = await message.reply_text(
        "ᴍᴏɴᴋᴇʏ ᴅ ʟᴜғғʏ\nɢᴇᴀʀ 𝟻..."
    )

    await asyncio.sleep(0.4)

    await m2.edit_text(
        "sᴜɴ ɢᴏᴅ ɴɪᴋᴀ!..."
    )

    await asyncio.sleep(0.5)

    await m2.delete()

    await asyncio.sleep(300)

    try:
        await sent.delete()
        await warn.delete()

    except:
        pass

# ONLY OWNER + ADMIN CAN UPLOAD 
@app.on_message(
    (filters.document | filters.video | filters.audio | filters.sticker | filters.animation) &
    filters.private
)
async def save_media(client, message: Message):

    # Allow only owner + admin
    if not (message.from_user.id == OWNER_ID or await is_admin(message.from_user.id)):
        return await message.reply_text("ғᴜᴄᴋ ʏᴏᴜ, ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ᴍᴀsᴛᴇʀ. ɢᴏ ᴀᴡᴀʏ, ʙɪᴛᴄʜ 🙃..")
        
    original_caption = message.caption if message.caption else ""

    # Detect file type
    if message.video:
        file = message.video
        file_type = "video"
        thumb = file.thumbs[-1].file_id if file.thumbs else None

    elif message.audio:
        file = message.audio
        file_type = "audio"
        thumb = None

    elif message.document:
        file = message.document
        file_type = "document"
        thumb = None

    elif message.sticker:
        file = message.sticker
        file_type = "sticker"
        thumb = None

    elif message.animation:  # GIF
        file = message.animation
        file_type = "animation"
        thumb = None

    else:
        return await message.reply_text("‼️ Uɴsᴜᴘᴘᴏʀᴛᴇᴅ Fᴏʀᴍᴀᴛ")

    file_id = file.file_id
    file_unique_id = file.file_unique_id

    await save_file(file_id, file_unique_id, file_type, original_caption, thumb)

    link = f"https://t.me/{BOT_USERNAME}?start={file_unique_id}"

    await message.reply_text(f"🔗 𝗛𝗲𝗿𝗲 𝗜𝘀 𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸:\n{link}")

# STATS
@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(client, message: Message):

    start = time.time()
    total = await total_users()

    uptime_seconds = int(time.time() - START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    ping = round((time.time() - start) * 1000)

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔄 Rᴇғʀᴇsʜ", callback_data="refresh_stats")]]
    )

    process = psutil.Process()
    memory = process.memory_info().rss / (1024 * 1024)

    await message.reply_text(
        f"📊 **𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝘂𝘀**\n\n"
        f"👥 Usᴇʀs: {total}\n"
        f"⏱ Uᴘᴛɪᴍᴇ: {hours}h {minutes}m {seconds}s\n"
        f"⚡ Pɪɴɢ: {ping} ms\n"
        f"🧠 Mᴇᴍᴏʀʏ Usᴀɢᴇ: {memory:.2f} MB\n"
        f"🧾 Vᴇʀsɪᴏɴ: {BOT_VERSION}",
        reply_markup=keyboard
    )


# BROADCAST
@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client, message: Message):

    if not message.reply_to_message:
        return await message.reply_text("Rᴇᴘʟʏ Tᴏ A Mᴇssᴀɢᴇ Tᴏ Bʀᴏᴀᴅᴄᴀsᴛ..")

    msg = message.reply_to_message

    users = await get_all_users()

    sent = 0
    failed = 0

    status = await message.reply_text("⏳️ 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗦𝘁𝗮𝗿𝘁𝗲𝗱.....")  

    for user_id in users:
        try:
            await msg.copy(chat_id=int(user_id))
            sent += 1
            await asyncio.sleep(0.2)

        except Exception as e:
            failed += 1
            print(f"Failed: {user_id} | {e}")

    await status.edit_text(
        f"⏳️ 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗖𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝗱\n\n"
        f"◇ Sᴜᴄᴄᴇssғᴜʟ: {sent}\n"
        f"◇ Uɴsᴜᴄᴄᴇssғᴜʟ: {failed}"
    )
    
@app.on_message(
    filters.private &
    ~filters.service &
    ~filters.command(["addadmin", "removeadmin", "adminlist"])
)
async def auto_add_user(client, message: Message):
    if message.from_user:
        await add_user(message.from_user.id)

# ADD ADMIN 
@app.on_message(filters.command("addadmin") & filters.private)
async def add_admin(client, message: Message):

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ᴍᴀsᴛᴇʀ. ɢᴏ ᴀᴡᴀʏ, ʙɪᴛᴄʜ 🙃..")

    if len(message.command) < 2:
        return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ /addadmin user_id")

    try:
        user_id = int(message.command[1])
    except:
        return await message.reply_text("‼️ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ")

    user = await client.get_users(user_id)

    name = user.first_name
    username = user.username if user.username else "None"

    await add_admin_db(user_id, name, username)

    await message.reply_text(f"✅️ ᴀᴅᴍɪɴ ɪs ᴀᴅᴅᴇᴅ : {user_id}")
    
    # Send message to that user
    try:
        await client.send_message(
            chat_id=user_id,
            text="🎉 ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs ʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ᴘʀᴏᴍᴏᴛᴇᴅ ᴛᴏ 𝗔𝗗𝗠𝗜𝗡\n\nYᴏᴜ ᴄᴀɴ ɴᴏᴡ ᴜᴘʟᴏᴀᴅ ғɪʟᴇs ᴛᴏ ᴛʜᴇ ʙᴏᴛ ᴀɴᴅ ɢᴇɴᴇʀᴀᴛᴇ ʟɪɴᴋs."
        )
    except Exception as e:
        print(f"Fᴀɪʟᴇᴅ Tᴏ Nᴏᴛɪғʏ Aᴅᴍɪɴ : {e}")
        
# REMOVE ADMIN 
@app.on_message(filters.command("removeadmin") & filters.private)
async def remove_admin(client, message: Message):

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ᴍᴀsᴛᴇʀ. ɢᴏ ᴀᴡᴀʏ, ʙɪᴛᴄʜ 🙃..")

    if len(message.command) < 2:
        return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ /removeadmin user_id")

    try:
        user_id = int(message.command[1])
    except:
        return await message.reply_text("‼️ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ")

    await remove_admin_db(user_id)

    await message.reply_text(f"✅️ ᴀᴅᴍɪɴ ɪs ʀᴇᴍᴏᴠᴇᴅ : {user_id}")

#ADMIN LIST
@app.on_message(filters.command("adminlist") & filters.private)
async def admin_list(client, message: Message):

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("🚫 Only owner can use this")

    admins = await get_all_admins()

    if not admins:
        return await message.reply_text("❌ No admins found")

    text = "👑 Admin List\n\n"

    for i, admin in enumerate(admins, start=1):
        name = admin.get("name", "Unknown")
        username = admin.get("username", "None")
        user_id = admin.get("user_id")

        text += (
            f"{i}. Name: {name}\n"
            f"   Username: @{username if username != 'None' else 'no_username'}\n"
            f"   ID: {user_id}\n\n"
        )

    await message.reply_text(text)
    
# ABOUT HANDLER
@app.on_callback_query(filters.regex("about"))
async def about_callback(client, query):
    await query.message.edit_text(
        "⍟───[ MY ᴅᴇᴛᴀɪʟꜱ ]───⍟\n\n"
        "‣ ᴍʏ ɴᴀᴍᴇ : [ᴀᴜ ʟᴜғғʏ sᴛᴏʀᴇ ʙᴏᴛ](https://t.me/AU_Luffy_Store_bot)\n"
        "‣ ᴅᴇᴠᴇʟᴏᴘᴇʀ : [ᴍᴏʜᴀᴍᴍᴇᴅ](https://t.me/Mr_Mohammed_29)\n"
        "‣ ʟɪʙʀᴀʀʏ : [ᴘʏʀᴏɢʀᴀᴍ 𝟸.𝟶](https://pypi.org/project/Pyrogram/)\n"
        "‣ ʟᴀɴɢᴜᴀɢᴇ : [ᴘʏᴛʜᴏɴ 𝟹](https://www.python.org/downloads/)\n"
        "‣ ᴅᴀᴛᴀ ʙᴀsᴇ : [ᴍᴏɴɢᴏ ᴅʙ](https://www.mongodb.com/)\n"
        "‣ ʙᴏᴛ sᴇʀᴠᴇʀ : [Bᴏᴛs Sᴇʀᴠᴇʀ](https://t.me/Anime_UpdatesAU)\n"
        "‣ ᴜᴘᴅᴀᴛᴇs : [ᴀɴɪᴍᴇ ᴜᴘᴅᴀᴛᴇs](https://t.me/Anime_UpdatesAU)\n"
        "‣ ʙᴜɪʟᴅ sᴛᴀᴛᴜs : ᴠ3.𝟶 [sᴛᴀʙʟᴇ](https://t.me/BotsServerDead)",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="home")]]
        ),
        parse_mode=ParseMode.MARKDOWN
    )


# HOME HANDLER
@app.on_callback_query(filters.regex("home"))
async def home_callback(client, query):

    photo = random.choice(IMAGES)

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=(
                "𝗛𝗲𝗹𝗹𝗼 ♡,\n\n"
                "›› 𝗜 𝗰𝗮𝗻 𝘀𝘁𝗼𝗿𝗲 𝗽𝗿𝗶𝘃𝗮𝘁𝗲 𝗳𝗶𝗹𝗲𝘀 𝗶𝗻 𝗦𝗽𝗲𝗰𝗶𝗳𝗶𝗲𝗱 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗮𝗻𝗱 𝗼𝘁𝗵𝗲𝗿 𝘂𝘀𝗲𝗿𝘀 𝗰𝗮𝗻 𝗮𝗰𝗰𝘀𝘀 𝗶𝘁 𝗳𝗿𝗼𝗺 𝘀𝗽𝗲𝗰𝗶𝗮𝗹 𝗹𝗶𝗻𝗸."
            ),
            parse_mode=ParseMode.MARKDOWN
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/Anime_UpdatesAU"),
                    InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about")
                ],
                [
                    InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/+ssaZDrj3Wr4wNzI1")
                ]
            ]
        )
    )

# REFRESH STATS 
@app.on_callback_query(filters.regex("refresh_stats"))
async def refresh_stats(client, query):

    start = time.time()
    total = await total_users()

    uptime_seconds = int(time.time() - START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    ping = round((time.time() - start) * 1000)

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔄 Rᴇғʀᴇsʜ", callback_data="refresh_stats")]]
    )

    process = psutil.Process()
    memory = process.memory_info().rss / (1024 * 1024)
    
    await query.message.edit_text(
        f"📊 **𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝘂𝘀**\n\n"
        f"👥 Usᴇʀs: {total}\n"
        f"⏱ Uᴘᴛɪᴍᴇ: {hours}h {minutes}m {seconds}s\n"
        f"⚡ Pɪɴɢ: {ping} ms\n"
        f"🧠 Mᴇᴍᴏʀʏ Usᴀɢᴇ: {memory:.2f} MB\n"
        f"🧾 Vᴇʀsɪᴏɴ: {BOT_VERSION}",
        reply_markup=keyboard
    )

    await query.answer("Sᴛᴀᴛs Uᴘᴅᴀᴛᴇᴅ 🔄")   
    
#RUN
keep_alive()
app.run()

#don't remove credits 
#Owner @Mr_Mohammed_29 
