# core/start_handler.py
from telegram import Update
from telegram.ext import ContextTypes
from core.broadcast_utils import save_user_if_not_exists
from core.inline_buttons import get_start_buttons
from core.start import get_welcome_message


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user_if_not_exists(user.id)  # ✅ Save user
    text = get_welcome_message(user)

    await update.message.reply_text(text=text,
                                    reply_markup=get_start_buttons(),
                                    parse_mode="HTML")
