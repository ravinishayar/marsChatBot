from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


# 🔘 START MENU BUTTONS
def get_start_buttons():
    keyboard = [[InlineKeyboardButton("📚 Help", callback_data="help_menu")],
                [
                    InlineKeyboardButton(
                        "➕ Add me to Group",
                        url="https://t.me/ChatManageHelpbot?startgroup=true")
                ]]
    return InlineKeyboardMarkup(keyboard)


# 🔘 HELP MENU BUTTONS (with GitHub Repo link instead of Auto Reply)
def get_help_buttons():
    keyboard = [
        [
            InlineKeyboardButton("📌 Commands", callback_data="commands"),
            InlineKeyboardButton("⚠️ Warning", callback_data="warn_info")
        ],
        [
            InlineKeyboardButton("🚫 Link Protection",
                                 callback_data="link_info"),
            InlineKeyboardButton(
                "📂 GitHub Repo",
                url="https://github.com/ravinishayar/marsChatBot.git"
            )  # 👈 Change URL here
        ],
        [
            InlineKeyboardButton("👨‍💻 Developer",
                                 url="https://t.me/ravinishayar54")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="start_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)


# 🔘 COMMAND BUTTONS (3 per row, no slashes)
def get_command_buttons():
    keyboard = [[
        InlineKeyboardButton("🚀 Start", callback_data="cmd_start"),
        InlineKeyboardButton("🎉 SetWelcome", callback_data="cmd_setwelcome"),
        InlineKeyboardButton("⚠️ Warn", callback_data="cmd_warn")
    ],
                [
                    InlineKeyboardButton("⛔ Ban", callback_data="cmd_ban"),
                    InlineKeyboardButton("✅ Unban", callback_data="cmd_unban"),
                    InlineKeyboardButton("🔇 Mute", callback_data="cmd_mute")
                ],
                [
                    InlineKeyboardButton("👢 Kick", callback_data="cmd_kick"),
                    InlineKeyboardButton("📢 Broadcast",
                                         callback_data="cmd_broadcast")
                ], [InlineKeyboardButton("🔙 Back", callback_data="help_menu")]]
    return InlineKeyboardMarkup(keyboard)


# 🔧 Safe Edit to avoid "Message is not modified" error
async def safe_edit(query, new_text, new_markup):
    if query.message.text == new_text and query.message.reply_markup == new_markup:
        return
    await query.edit_message_text(new_text,
                                  reply_markup=new_markup,
                                  parse_mode="HTML")


# ✅ Callback handler
async def handle_button_click(update: Update,
                              context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "help_menu":
        await safe_edit(query, "🧠 <b>Help Menu</b>\nChoose an option below:",
                        get_help_buttons())

    elif query.data == "commands":
        await safe_edit(query, "<b>📌 Choose a command to view its usage:</b>",
                        get_command_buttons())

    elif query.data == "cmd_start":
        await safe_edit(
            query,
            "🚀 <b>Start</b>\nStarts the bot and shows the welcome message.",
            get_command_buttons())

    elif query.data == "cmd_setwelcome":
        await safe_edit(
            query,
            "🎉 <b>SetWelcome</b>\nSets the welcome message for your group.",
            get_command_buttons())

    elif query.data == "cmd_warn":
        await safe_edit(
            query,
            "⚠️ <b>Warn</b>\nReply to a user's message with this command.\nAfter 2 warnings, they will be banned.",
            get_command_buttons())

    elif query.data == "cmd_ban":
        await safe_edit(
            query, "⛔ <b>Ban</b>\nBan a user via reply, username, or user ID.",
            get_command_buttons())

    elif query.data == "cmd_unban":
        await safe_edit(query,
                        "✅ <b>Unban</b>\nUnban a previously banned user.",
                        get_command_buttons())

    elif query.data == "cmd_mute":
        await safe_edit(
            query, "🔇 <b>Mute</b>\nMute a member using this command in reply.",
            get_command_buttons())

    elif query.data == "cmd_kick":
        await safe_edit(
            query,
            "👢 <b>Kick</b>\nRemove a user from group (they can rejoin).",
            get_command_buttons())

    elif query.data == "cmd_broadcast":
        await safe_edit(query,
                        "📢 <b>Broadcast</b>\nSend a message to all users.",
                        get_command_buttons())

    elif query.data == "warn_info":
        await safe_edit(
            query,
            "⚠️ <b>Warning System</b>\nUse 'Warn' to warn users. 2 warnings = auto ban.",
            get_help_buttons())

    elif query.data == "link_info":
        await safe_edit(
            query,
            "🚫 <b>Link Protection</b>\nAuto-deletes messages that contain links.",
            get_help_buttons())

    elif query.data == "start_menu":
        await safe_edit(query,
                        "👋 <b>Welcome back!</b>\nChoose an option below:",
                        get_start_buttons())
