from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


def get_start_buttons():
    keyboard = [[InlineKeyboardButton("📚 Help", callback_data="help_menu")],
                [
                    InlineKeyboardButton(
                        "➕ Add me to Group",
                        url="https://t.me/ChatManageHelpbot?startgroup=true")
                ]]
    return InlineKeyboardMarkup(keyboard)


def get_help_buttons():
    keyboard = [
        [InlineKeyboardButton("📌 Commands", callback_data="commands")],
        [InlineKeyboardButton("⚠️ Warning System", callback_data="warn_info")],
        [InlineKeyboardButton("🚫 Link Protection", callback_data="link_info")],
        [InlineKeyboardButton("🔄 Auto Reply", callback_data="reply_info")],
        [InlineKeyboardButton("🔙 Back", callback_data="start_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)


# ✅ Callback handler for inline buttons
async def handle_button_click(update: Update,
                              context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "help_menu":
        await query.edit_message_text(
            "🧠 <b>Help Menu</b>\nनीचे से कोई विकल्प चुनें:",
            reply_markup=get_help_buttons(),
            parse_mode="HTML")

    elif query.data == "commands":
        await query.edit_message_text(
            "<b>📌 Bot Commands</b>\n"
            "/start - Start the bot\n"
            "/setwelcome - Set welcome message\n"
            "/warn - Warn users\n"
            "/broadcast - Broadcast to users\n"
            "/broadcast_groups - Broadcast to groups",
            parse_mode="HTML",
            reply_markup=get_help_buttons())

    elif query.data == "warn_info":
        await query.edit_message_text(
            "⚠️ <b>Warning System</b>\n"
            "Reply to a user's message with /warn to issue warning.\n"
            "After 2 warnings, user will be banned.",
            parse_mode="HTML",
            reply_markup=get_help_buttons())

    elif query.data == "link_info":
        await query.edit_message_text(
            "🚫 <b>Link Protection</b>\n"
            "Messages containing links are auto-deleted, even from bots.",
            parse_mode="HTML",
            reply_markup=get_help_buttons())

    elif query.data == "reply_info":
        await query.edit_message_text(
            "🔄 <b>Auto Reply</b>\n"
            "Bot will automatically respond to common phrases or emoji.",
            parse_mode="HTML",
            reply_markup=get_help_buttons())

    elif query.data == "start_menu":
        await query.edit_message_text(
            "👋 <b>Welcome back!</b>\nChoose an option below:",
            reply_markup=get_start_buttons(),
            parse_mode="HTML")
