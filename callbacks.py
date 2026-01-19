from pyrogram import Client, filters
from pyrogram.types import Message
from keyboards import start_buttons, premium_buttons, quick_menu, queue_buttons


@Client.on_message(filters.text & filters.private)
async def button_handler(client: Client, message: Message):
    text = message.text.strip()

    if text == "🚀 Plan" or text == "/plan":
        await message.reply(
            "**💎 PREMIUM BENEFITS - UNLOCK THE FULL POWER!**\n\n"
            "✨ Unlimited Downloads\n"
            "⚡ Instant Processing\n"
            "🚀 Queue up to 20 URLs\n"
            "📦 2GB File Support\n"
            "🎯 Priority Processing\n"
            "🚫 No Ads\n\n"
            "👇 Choose a plan:",
            reply_markup=premium_buttons
        )

    elif text == "💎 Premium":
        await message.reply("Choose your premium plan:", reply_markup=premium_buttons)

    elif text == "👉 Quick Menu":
        await message.reply("📋 Quick Menu", reply_markup=quick_menu)

    elif text == "📂 My Queue":
        await message.reply("📂 Your Queue is empty.", reply_markup=queue_buttons)

    elif text == "🤝 Share Bot":
        await message.reply(
            "Share this bot with friends:\n\n"
            "https://t.me/YourBotUsername"
        )

    elif text == "❓ How to Use":
        await message.reply(
            "🔍 **How to Use This Bot**\n\n"
            "1️⃣ Join our channel\n"
            "2️⃣ Send a TeraBox link\n"
            "3️⃣ Download your file\n\n"
            "⚠ Send only one link at a time."
        )

    elif text == "❌ Cancel":
        await message.reply("Cancelled.", reply_markup=start_buttons)
