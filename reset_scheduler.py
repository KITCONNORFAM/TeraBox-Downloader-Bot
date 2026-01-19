import asyncio
from datetime import datetime, timedelta
import pytz
from database import USERS

IST = pytz.timezone("Asia/Kolkata")


async def reset_daily_limits():
    while True:
        now = datetime.now(IST)

        # Calculate next 12:00 AM IST
        next_reset = (now + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        wait_seconds = (next_reset - now).total_seconds()

        print(f"[Scheduler] Next reset at: {next_reset}")
        await asyncio.sleep(wait_seconds)

        # Reset all users
        for user_id in USERS:
            USERS[user_id]["count"] = 0
            USERS[user_id]["date"] = datetime.now(IST).date()

        print("[Scheduler] Daily limits reset successfully!")
