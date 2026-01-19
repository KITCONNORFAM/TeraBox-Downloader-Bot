import re
import aiohttp
from datetime import datetime, timedelta
from config import TERABOX_API_TEMPLATE, PRIVATE_CHAT_ID
from database import (
    is_premium,
    get_daily_count,
    increase_daily_count,
    can_download,
    add_to_queue,
    get_queue,
    clear_queue
)

TERABOX_REGEX = r"(https?://(www\.)?terabox\.com/\S+)"

# ================== LINK DETECTOR ==================

def extract_terabox_link(text):
    match = re.search(TERABOX_REGEX, text)
    return match.group(1) if match else None


# ================== DOWNLOAD HANDLER ==================

async def handle_link(client, message):
    user_id = message.from_user.id
    link = extract_terabox_link(message.text)

    if not link:
        return await message.reply("❌ Invalid TeraBox link.")

    # Free user limit check
    if not is_premium(user_id):
        if not can_download(user_id):
            return await message.reply(
                "⏳ Daily limit reached!\n\n"
                "You can download only *3 videos per day*.\n"
                "Try again after **12:00 AM IST** or get Premium 💎"
            )

    # Add to queue
    add_to_queue(user_id, link)
    await message.reply("📂 Added to queue...\n⏬ Processing now...")

    await process_queue(client, user_id, message)


# ================== QUEUE PROCESSOR ==================

async def process_queue(client, user_id, message):
    queue = get_queue(user_id)

    if not queue:
        return

    link = queue[0]

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(TERABOX_API_TEMPLATE.format(url=link)) as resp:
                data = await resp.json()

        if not data.get("success"):
            return await message.reply("❌ Failed to fetch video.")

        file_url = data["data"]["download_url"]
        file_name = data["data"]["file_name"]

        sent = await client.send_file(
            PRIVATE_CHAT_ID,
            file_url,
            caption=file_name
        )

        await client.send_file(
            message.chat.id,
            sent.media,
            caption=f"✅ Downloaded: {file_name}"
        )

        # Increase count for free users
        if not is_premium(user_id):
            increase_daily_count(user_id)

        # Remove from queue
        clear_queue(user_id, first_only=True)

    except Exception as e:
        await message.reply(f"⚠️ Error: {str(e)}")
