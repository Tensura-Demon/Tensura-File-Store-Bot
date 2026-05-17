from pyrogram import Client
from config import API_ID, API_HASH

CLONES = {}

async def start_clone(user_id, bot_token):

    if user_id in CLONES:
        raise Exception("You already have a clone running")

    bot = Client(
        name=f"clone_{user_id}",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=bot_token,
        in_memory=True
    )

    await bot.start()

    me = await bot.get_me()

    CLONES[user_id] = bot

    print(f"Clone Started @{me.username}")

    return me.username


async def stop_clone(user_id):

    bot = CLONES.get(user_id)

    if not bot:
        return False

    await bot.stop()

    del CLONES[user_id]

    print(f"Clone Stopped {user_id}")

    return True
