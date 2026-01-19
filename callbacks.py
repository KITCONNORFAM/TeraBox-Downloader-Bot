from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================= PLAN MENU =================

@Client.on_callback_query(filters.regex("^plan$"))
async def plan_cb(_, query):
    await query.message.edit_text(
        """💰 Premium Plans:

🔥 TRIAL – ₹29 | 7 days | ₹4/day
🎯 STARTER – ₹49 | 15 days | ₹3.3/day
💎 POPULAR – ₹79 | 30 days | ₹2.6/day
⭐ BEST VALUE – ₹149 | 75 days | ₹2/day
👑 VIP CLUB – ₹199 | 120 days | ₹1.6/day
♾️ YEARLY – ₹399 | 365 days | ₹1/day""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔥 TRIAL", callback_data="plan_trial")],
            [InlineKeyboardButton("🎯 STARTER", callback_data="plan_starter")],
            [InlineKeyboardButton("💎 POPULAR", callback_data="plan_popular")],
            [InlineKeyboardButton("⭐ BEST VALUE", callback_data="plan_bestvalue")],
            [InlineKeyboardButton("👑 VIP CLUB", callback_data="plan_vip")],
            [InlineKeyboardButton("♾️ YEARLY", callback_data="plan_yearly")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
        ])
    )

# ================= PAYMENT INFO =================

@Client.on_callback_query(filters.regex("^plan_"))
async def payment_info(_, query):
    plan = query.data.replace("plan_", "")

    await query.message.edit_text(
        f"""💳 *Payment for {plan.upper()} Plan*

Send payment via UPI / QR  
Then send screenshot to:

👑 Owner: @charliespringfam  
👑 Backup: @Badmaashbachhax  

After verification, premium will be activated manually.

⏳ Processing time: 5–30 minutes
""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅ Back", callback_data="plan")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
        ])
    )

# ================= CANCEL =================

@Client.on_callback_query(filters.regex("^cancel$"))
async def cancel_cb(_, query):
    await query.message.edit_text(
        "❌ Cancelled.\n\nUse /start to open menu again."
    )

# ================= HOW TO USE =================

@Client.on_callback_query(filters.regex("^how$"))
async def how_cb(_, query):
    await query.message.edit_text(
        """🔍 How to Use This Bot

1️⃣ Join our channel  
2️⃣ Send TeraBox link  
3️⃣ Get your file  

⚠ Only one link at a time""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅ Back", callback_data="menu")]
        ])
    )

# ================= QUICK MENU =================

@Client.on_callback_query(filters.regex("^menu$"))
async def menu_cb(_, query):
    await query.message.edit_text(
        "👉 Quick Menu",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Plan", callback_data="plan")],
            [InlineKeyboardButton("❓ How to Use", callback_data="how")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
        ])
    )

# ================= SHARE BOT =================

@Client.on_callback_query(filters.regex("^share$"))
async def share_cb(_, query):
    await query.message.edit_text(
        "🤝 Share this bot:\n\nhttps://t.me/YourBotUsername",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅ Back", callback_data="menu")]
        ])
    )
