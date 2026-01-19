import asyncio
import os
import time
from uuid import uuid4
from datetime import datetime
import pytz

import redis
import telethon
from telethon import TelegramClient, events, Button
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.types import Message, UpdateNewMessage

from cansend import CanSend
from config import *
from terabox import get_data   # ❗ UNTOUCHED
from tools import (
    convert_seconds,
    download_file,
    download_image_to_bytesio,
    extract_code_from_url,
    get_formatted_size,
    get_urls_from_string,
    is_user_on_chat,
)

bot = TelegramClient("tele", API_ID, API_HASH)

db = redis.Redis(
    host=HOST,
    port=PORT,
    password=PASSWORD,
    decode_responses=True,
)

PREMIUM_USERS_KEY = "premium_users"
DAILY_LIMIT_KEY = "daily_limit"

IST = pytz.timezone("Asia/Kolkata")

# ================== HELPERS ==================

def is_owner(uid):
    return uid in OWNERS

def is_admin(uid):
    return uid in ADMINS or uid in OWNERS

def today_key(uid):
    today = datetime.now(IST).strftime("%Y-%m-%d")
    return f"{DAILY_LIMIT_KEY}:{uid}:{today}"

def can_download(uid):
    if db.sismember(PREMIUM_USERS_KEY, uid):
        return True, "premium"

    key = today_key(uid)
    used = int(db.get(key) or 0)

    if used >= 3:
        return False, "limit"

    db.incr(key)
    db.expire(key, 86400)
    return True, "free"

# ================== /START ==================

@bot.on(events.NewMessage(pattern="/start", incoming=True))
async def start(m: UpdateNewMessage):
    user = await bot.get_entity(m.sender_id)

    text = f"""
Welcome back to Tera Box Bots!!

👤 Hi {user.first_name}!

🔄 Just send me any TeraBox link, and I'll download it for you instantly.
"""

    buttons = [
        [Button.text("🚀 Plan"), Button.text("📂 My Queue")],
        [Button.text("🤝 Share Bot"), Button.text("💎 Premium")],
        [Button.text("❓ How to Use"), Button.text("👑 Get Premium (No Ads)")],
        [Button.text("👉 Quick Menu")],
    ]

    await m.reply(text, buttons=buttons)

# ================== HELP ==================

@bot.on(events.NewMessage(pattern="/help", incoming=True))
async def help_cmd(m):
    await m.reply("""
Available Commands:

/start - Start bot  
/help - Help menu  
/plan - Premium plans  
/status - Your plan  
/redeem - Redeem code  

Free Users:
• 3 downloads/day  
• Reset at 12:00 AM IST  

Premium:
• Unlimited  
• No ads  
• Priority  

Support:
@charliespringfam  
@Badmaashbachhax
""")

# ================== PLAN ==================

@bot.on(events.NewMessage(pattern="/plan", incoming=True))
async def plan(m):
    await m.reply("""
💎 PREMIUM PLANS

🔥 TRIAL – ₹29 | 7 days  
🎯 STARTER – ₹49 | 15 days  
💎 POPULAR – ₹79 | 30 days  
⭐ BEST VALUE – ₹149 | 75 days  
👑 VIP CLUB – ₹199 | 120 days  
♾️ YEARLY – ₹399 | 365 days  

To buy:  
@charliespringfam  
@Badmaashbachhax
""")

# ================== STATUS ==================

@bot.on(events.NewMessage(pattern="/status", incoming=True))
async def status(m):
    uid = m.sender_id
    if db.sismember(PREMIUM_USERS_KEY, uid):
        await m.reply("💎 You are a PREMIUM user")
    else:
        used = int(db.get(today_key(uid)) or 0)
        await m.reply(f"🆓 Free User\nDownloads used today: {used}/3")

# ================== ADMIN COMMANDS ==================

@bot.on(events.NewMessage(pattern="/addadmin (.*)", from_users=OWNERS))
async def add_admin(m):
    new = int(m.pattern_match.group(1))
    if new not in ADMINS:
        ADMINS.append(new)
        await m.reply(f"✅ Added admin {new}")

@bot.on(events.NewMessage(pattern="/removeadmin (.*)", from_users=OWNERS))
async def rem_admin(m):
    rem = int(m.pattern_match.group(1))
    if rem in ADMINS:
        ADMINS.remove(rem)
        await m.reply(f"❌ Removed admin {rem}")

@bot.on(events.NewMessage(pattern="/pre (.*)", from_users=ADMINS))
async def add_premium(m):
    uid = int(m.pattern_match.group(1))
    db.sadd(PREMIUM_USERS_KEY, uid)
    await m.reply("User promoted to premium")

@bot.on(events.NewMessage(pattern="/de (.*)", from_users=ADMINS))
async def remove_premium(m):
    uid = int(m.pattern_match.group(1))
    db.srem(PREMIUM_USERS_KEY, uid)
    await m.reply("User removed from premium")

# ================== QUEUE ==================

@bot.on(events.NewMessage(pattern="/queue", incoming=True))
async def show_queue(m):
    uid = m.sender_id
    q = db.lrange(f"queue:{uid}", 0, -1)
    if not q:
        return await m.reply("📭 Queue empty")

    text = "\n".join([f"{i+1}. {x}" for i, x in enumerate(q)])
    await m.reply(f"📦 Your Queue:\n{text}")

# ================== DOWNLOAD HANDLER ==================

@bot.on(events.NewMessage(incoming=True, func=lambda m: m.text and get_urls_from_string(m.text)))
async def downloader(m: Message):
    uid = m.sender_id

    allowed, status = can_download(uid)

    if not allowed:
        await m.reply("❌ Daily limit reached.\nWait till 12:00 AM IST or buy premium.")
        return

    url = get_urls_from_string(m.text)
    await m.reply("⏳ Processing your link...")

    data = get_data(url)   # ❗ UNTOUCHED COOKIE LOGIC

    if not data:
        return await m.reply("❌ API error or invalid link.")

    await bot.send_message(
        PRIVATE_CHAT_ID,
        f"User {uid} downloaded: {data['file_name']}"
    )

    await m.reply(f"✅ Download ready:\n{data['file_name']}")

# ================== START BOT ==================

bot.start(bot_token=BOT_TOKEN)
bot.run_until_disconnected()
