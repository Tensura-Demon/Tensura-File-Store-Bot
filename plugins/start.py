from pyrogram import Client, filters

@Client.on_message(filters.command("start"))
async def start_cmd(client, message):

    await message.reply_text(
        "✅ WelcomE To Your Bot"
    )


@Client.on_message(filters.command("ping"))
async def ping_cmd(client, message):

    await message.reply_text("🏓 Pong")
