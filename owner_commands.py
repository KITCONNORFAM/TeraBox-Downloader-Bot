from pyrogram import Client, filters

ADMINS = [803003146]  # Apna Telegram ID

# Promote to Premium
@Client.on_message(filters.command("pre") & filters.user(ADMINS))
async def promote(_, message):
    user_id = message.text.split(" ")[1]
    await message.reply(f"✅ {user_id} promoted to Premium.")

# Demote Premium
@Client.on_message(filters.command("de") & filters.user(ADMINS))
async def demote(_, message):
    user_id = message.text.split(" ")[1]
    await message.reply(f"❌ {user_id} removed from Premium.")

# Broadcast
@Client.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def broadcast(_, message):
    text = message.text.replace("/broadcast", "")
    await message.reply("📢 Broadcast sent!")

# Premium Users List
@Client.on_message(filters.command("premium_users") & filters.user(ADMINS))
async def premium_list(_, message):
    await message.reply("📋 Premium users list here.")

# Gift Code Generate
@Client.on_message(filters.command("gc") & filters.user(ADMINS))
async def gift_code(_, message):
    await message.reply("🎁 Gift codes generated.")

# Ping
@Client.on_message(filters.command("ping"))
async def ping(_, message):
    await message.reply("🏓 Pong!")
