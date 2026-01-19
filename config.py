# ================== TELEGRAM API CONFIG ==================

# Get these from https://my.telegram.org/apps
API_ID = 1234567
API_HASH = "YOUR_API_HASH_HERE"

# Bot token from @BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"


# ================== REDIS DATABASE CONFIG ==================

# Redis Host / Port / Password
HOST = "127.0.0.1"
PORT = 6379
PASSWORD = None   # Set to None if Redis has no password


# ================== BOT SETTINGS ==================

# Private storage chat where files are uploaded
# Use your private channel / chat ID (must be integer)
PRIVATE_CHAT_ID = -1000000000000


# ================== OWNER & ADMIN SYSTEM ==================

# Full control (2–3 numeric IDs supported)
OWNERS = [
    803003146,
    # 987654321,
    # 1122334455
]

# Limited control
ADMINS = [
    803003146,
    # 555666777
]


# ================== FREE USER LIMIT SYSTEM ==================

FREE_DAILY_LIMIT = 3
TIMEZONE = "Asia/Kolkata"
RESET_AT_MIDNIGHT = True


# ================== TERABOX API CONFIG ==================

TERABOX_API_BASE = "https://api.ntm.com/api/terabox"
TERABOX_API_TOKEN = "NTMPASS"

TERABOX_API_TEMPLATE = (
    f"{TERABOX_API_BASE}?key={TERABOX_API_TOKEN}&url={{url}}"
)
