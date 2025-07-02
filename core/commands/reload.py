from telegram import Update
from telegram.ext import ContextTypes


async def reload_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Example logic for reloading admin list
    await update.message.reply_text("✅ Admin list reloaded.")
