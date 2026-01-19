from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================= START =================

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(_, message):
    user = message.from_user.first_name

    await message.reply(
        f"""Welcome back to Tera Box Bots!!

👤 Hi {user}!

🔄 Just send me any TeraBox link, and I'll download it for you instantly.""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Plan", callback_data="plan"),
             InlineKeyboardButton("📂 My Queue", callback_data="queue")],
            [InlineKeyboardButton("🤝 Share Bot", callback_data="share"),
             InlineKeyboardButton("💎 Premium", callback_data="plan")],
            [InlineKeyboardButton("❓ How to Use", callback_data="how"),
             InlineKeyboardButton("👑 Get Premium (No Ads)", callback_data="plan")],
            [InlineKeyboardButton("👉 Quick Menu", callback_data="menu")]
        ])
    )

# ================= HELP =================

@Client.on_message(filters.command("help") & filters.private)
async def help_cmd(_, message):
    await message.reply(
        """❓ Help Menu

Send any TeraBox link to download.

Commands:
/start - Start bot  
/plan - View plans  
/status - Account info  
/limits - Free limits  
/support - Contact support  
"""
    )

# ================= PLAN =================

@Client.on_message(filters.command("plan") & filters.private)
async def plan_cmd(_, message):
    await message.reply(
        "Click below to view premium plans:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 View Plans", callback_data="plan")]
        ])
    )

# ================= STATUS =================

@Client.on_message(filters.command("status") & filters.private)
async def status_cmd(_, message):
    await message.reply(
        """📊 Your Status

Premium: ❎  
Free Downloads: 3/3  
Queue Limit: 2  
"""
    )

# ================= LIMITS =================

@Client.on_message(filters.command("limits") & filters.private)
async def limits_cmd(_, message):
    await message.reply(
        """🆓 Free User Limits

• 3 videos per day  
• Reset at 12:00 AM IST  
• Max 500MB per file  
"""
    )

# ================= BUY =================

@Client.on_message(filters.command("buy") & filters.private)
async def buy_cmd(_, message):
    await message.reply(
        "Choose your premium plan:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 View Plans", callback_data="plan")]
        ])
    )

# ================= SUPPORT =================

@Client.on_message(filters.command("support") & filters.private)
async def support_cmd(_, message):
    await message.reply(
        """💬 Contact Support

👑 @charliespringfam  
Backup: @Badmaashbachhax  
"""
    )
