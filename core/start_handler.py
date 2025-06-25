import os
from telegram import Update
from telegram.ext import ContextTypes
from core.inline_buttons import get_start_buttons
from core.broadcast_utils import save_user  # ✅ Make sure this exists

BOT_TOKEN = os.getenv("BOT_TOKEN")
LOGGER_GROUP_ID = os.getenv("LOGGER_GROUP_ID")  # Add this in Secrets


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_url = "https://files.catbox.moe/tinlr0.jpg"
    caption = ("👋 <b>नमस्ते!</b> मैं आपका <b>MarsGroupManager</b> 🤖 हूँ।\n"
               "📌 Auto-reply, link protection, welcome, warning & more!\n\n"
               "👇 मुझे अपने ग्रुप में जोड़ें और कमाल देखें:")

    # ✅ Save user or group ID for broadcast
    save_user(update.effective_chat.id)

    # ✅ Send image, caption and inline buttons
    await update.message.reply_photo(photo=image_url,
                                     caption=caption,
                                     reply_markup=get_start_buttons(),
                                     parse_mode="HTML")

    # ✅ Log to LOGGER_GROUP_ID if available
    user = update.effective_user
    if LOGGER_GROUP_ID:
        log_msg = (f"🚀 <b>New /start</b>\n"
                   f"👤 Name: {user.full_name}\n"
                   f"🔗 Username: @{user.username or 'N/A'}\n"
                   f"🆔 User ID: <code>{user.id}</code>")
        try:
            await context.bot.send_message(chat_id=int(LOGGER_GROUP_ID),
                                           text=log_msg,
                                           parse_mode="HTML")
        except Exception as e:
            print(f"❌ Logger error: {e}")
