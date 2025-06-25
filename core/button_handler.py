from telegram import Update
from telegram.ext import ContextTypes
from core.inline_buttons import get_help_buttons, get_start_buttons


async def handle_button_click(update: Update,
                              context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        if query.data == "help_menu":
            text = ("🛠 <b>Commands List</b>\n"
                    "• /start - बॉट शुरू करें\n"
                    "• /setwelcome - वेलकम मैसेज सेट करें\n"
                    "• /warn - यूजर को चेतावनी दें\n"
                    "• /broadcast - यूज़र्स को ब्रॉडकास्ट भेजें\n"
                    "• /broadcast_groups - ग्रुप्स को ब्रॉडकास्ट भेजें\n"
                    "• /help - सहायता लें")
            if query.message.text:
                await query.edit_message_text(text=text,
                                              parse_mode="HTML",
                                              reply_markup=get_help_buttons())
            else:
                await query.message.reply_text(text=text,
                                               parse_mode="HTML",
                                               reply_markup=get_help_buttons())

        elif query.data == "start_menu":
            text = ("👋 <b>Welcome Back!</b>\n"
                    "👇 नीचे दिए गए बटन से शुरू करें:")
            if query.message.text:
                await query.edit_message_text(text=text,
                                              parse_mode="HTML",
                                              reply_markup=get_start_buttons())
            else:
                await query.message.reply_text(
                    text=text,
                    parse_mode="HTML",
                    reply_markup=get_start_buttons())

    except Exception as e:
        print(f"❌ Error editing message: {e}")
