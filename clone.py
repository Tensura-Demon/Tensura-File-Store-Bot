from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH

CLONES = {}

async def start_clone(user_id, bot_token):

    if user_id in CLONES:
        raise Exception("Clone already running")

    bot = Client(
        name=f"clone_{user_id}",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=bot_token,
        workdir="sessions"
    )

    @bot.on_message(filters.command("start"))
    async def start_cmd(client, message: Message):

        await message.reply_text(
            "✅ Clone Bot Active"
        )

    @bot.on_message(filters.command("ping"))
    async def ping_cmd(client, message: Message):

        await message.reply_text("🏓 Pong")

    await bot.start()

    me = await bot.get_me()

    CLONES[user_id] = bot

    print(f"Started Clone @{me.username}")

    return me.username


async def stop_clone(user_id):

    if user_id not in CLONES:
        return

    bot = CLONES[user_id]

    await bot.stop()

    del CLONES[user_id]
