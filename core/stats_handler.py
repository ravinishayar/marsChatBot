# core/stats_handler.py

import time
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from core.database import get_user_collection

# Bot start time
BOT_START_TIME = time.time()


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = get_user_collection()
    total_users = users.count_documents({})

    uptime = time.time() - BOT_START_TIME
    uptime_str = format_uptime(uptime)

    await update.message.reply_html(
        f"<b>📊 Bot Stats:</b>\n\n"
        f"👥 <b>Total Users:</b> <code>{total_users}</code>\n"
        f"⏱ <b>Uptime:</b> <code>{uptime_str}</code>\n"
        f"👨‍💻 <b>Developer:</b> <a href='https://t.me/ravinishayar54'>@ravinishayar54</a>\n"
        f"📢 <b>Support:</b> <a href='https://t.me/GroupHelpChatGuard'>GroupHelpChatGuard</a>"
    )


def format_uptime(seconds: float) -> str:
    mins, secs = divmod(int(seconds), 60)
    hours, mins = divmod(mins, 60)
    days, hours = divmod(hours, 24)
    return f"{days}d {hours}h {mins}m {secs}s"


# Export command handler
stats_handler = CommandHandler("stats", stats_command)
