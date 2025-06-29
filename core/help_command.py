from telegram import Update
from telegram.ext import ContextTypes
from core.inline_buttons import get_help_buttons  # 🧠 Import the interactive help menu


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "🧠 <b>Help Menu</b>\nनीचे से कोई विकल्प चुनें:",
            reply_markup=get_help_buttons(),
            parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            "🧠 <b>Help Menu</b>\nनीचे से कोई विकल्प चुनें:",
            reply_markup=get_help_buttons(),
            parse_mode="HTML")
