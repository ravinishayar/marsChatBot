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

    # ✅ 1. Broadcast list में user को save करें
    save_user(update.effective_chat.id)

    # ✅ 2. फोटो + caption + बटन भेजें
    await update.message.reply_photo(photo=image_url,
                                     caption=caption,
                                     reply_markup=get_start_buttons(),
                                     parse_mode="HTML")

    # ✅ 3. LOGGER_GROUP_ID में log भेजें (अगर सेट है)
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
