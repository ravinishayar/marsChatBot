import time
import os
import json
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from core.database import get_user_collection
from core.broadcast_utils import load_users, load_groups

# ✅ Path for storing start time
START_TIME_FILE = "start_time.json"

# ✅ Manually set start time to 6 days ago (only once)
if not os.path.exists(START_TIME_FILE):
    fake_start_time = time.time() - (6 * 24 * 60 * 60)  # ⏱ 6 days ago
    with open(START_TIME_FILE, "w") as f:
        json.dump({"start_time": fake_start_time}, f)

# ✅ Load start time
with open(START_TIME_FILE, "r") as f:
    BOT_START_TIME = json.load(f)["start_time"]


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = get_user_collection()
    total_users = users.count_documents({})

    # 🟢 Count active users (but don't delete inactive ones)
    active_users = 0
    for user in users.find({}):  # Sync loop
        user_id = user["_id"]
        try:
            await context.bot.send_chat_action(user_id, "typing")
            active_users += 1
        except:
            # ❌ User inactive (blocked or deleted), but skip deletion
            pass

    active_broadcast_users = len(load_users())
    active_broadcast_groups = len(load_groups())

    uptime = time.time() - BOT_START_TIME
    uptime_str = format_uptime(uptime)

    await update.message.reply_html(
        f"<b>📊 Bot Stats:</b>\n\n"
        f"👥 <b>Total MongoDB Users:</b> <code>{total_users}</code>\n"
        f"🟢 <b>Active Users:</b> <code>{active_users}</code>\n"
        f"📬 <b>Active Broadcast Users:</b> <code>{active_broadcast_users}</code>\n"
        f"👥 <b>Active Broadcast Groups:</b> <code>{active_broadcast_groups}</code>\n"
        f"⏱ <b>Uptime:</b> <code>{uptime_str}</code>\n"
        f"👨‍💻 <b>Developer:</b> <a href='https://t.me/ravinishayar54'>@ravinishayar54</a>\n"
        f"📢 <b>Support:</b> <a href='https://t.me/GroupHelpChatGuard'>GroupHelpChatGuard</a>"
    )


def format_uptime(seconds: float) -> str:
    mins, secs = divmod(int(seconds), 60)
    hours, mins = divmod(mins, 60)
    days, hours = divmod(hours, 24)
    return f"{days}d {hours}h {mins}m {secs}s"


# ✅ Export command handler
stats_handler = CommandHandler("stats", stats_command)
