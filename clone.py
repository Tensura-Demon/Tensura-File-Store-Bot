from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH

CLONES = {}

async def start_clone(user_id, bot_token):

    clone = Client(
        name=f"clone_{user_id}",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=bot_token
    )

    await clone.start()

    me = await clone.get_me()

    CLONES[user_id] = clone

    @clone.on_message(filters.command("start"))
    async def clone_start(client, message):

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📝 START MESSAGE",
                        callback_data="startmsg"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "👥 ADMINS",
                        callback_data="admins"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📊 BOT STATUS",
                        callback_data="status"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⚙️ MORE FEATURES",
                        callback_data="features"
                    )
                ]
            ]
        )

        await message.reply_text(
            f"🤖 Welcome To @{me.username}",
            reply_markup=buttons
        )

    @clone.on_callback_query(filters.regex("features"))
    async def features(client, query):

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🍿 CUSTOM CAPTION",
                        callback_data="caption"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📢 FORCE SUBSCRIBE",
                        callback_data="forcesub"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🖼 THUMBNAIL",
                        callback_data="thumb"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "♻️ AUTO DELETE",
                        callback_data="autodelete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔒 PROTECT CONTENT",
                        callback_data="protect"
                    )
                ]
            ]
        )

        await query.message.edit_text(
            "⚙️ CLONE SETTINGS",
            reply_markup=buttons
        )

    return me.username


async def stop_clone(user_id):

    if user_id in CLONES:

        await CLONES[user_id].stop()

        del CLONES[user_id]
