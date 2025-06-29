import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ChatMemberHandler,
    filters,
)

# 🔁 Core Logic Imports
from core import (
    start,
    handle_chat_messages,
    set_welcome_start,
    save_welcome_message,
    welcome_new_member,
    welcome_on_add,
)

from core.help_command import help_command
from core.inline_buttons import handle_button_click  # ✅ Inline help callback handler
from core.warnsystem import get_warn_handler  # ⚠️ Warning system
from core.link_protection import auto_delete_links  # 🔗 Link deletion
from core.broadcast import broadcast_command  # 📢 Broadcast to users
from core.group_broadcast import broadcast_groups, get_group_broadcast_handler  # 📢 Broadcast to groups
from core.ban_handler import ban_user, unban_user  # ✅ /ban & /unban commands
from core.moderation import mute_user, kick_user  # ✅ /mute & /kick commands

# 🔐 Bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ✅ Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))  # Inline help entry
    app.add_handler(CommandHandler("setwelcome", set_welcome_start))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(get_group_broadcast_handler())
    app.add_handler(get_warn_handler())
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("unban", unban_user))
    app.add_handler(CommandHandler("mute", mute_user))  # 🔇 Added
    app.add_handler(CommandHandler("kick", kick_user))  # 👢 Added

    # 🔘 Inline Button Callback Handler
    app.add_handler(CallbackQueryHandler(handle_button_click))

    # 👥 New Chat Members
    app.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS,
                       welcome_new_member))
    app.add_handler(
        ChatMemberHandler(welcome_on_add, ChatMemberHandler.MY_CHAT_MEMBER))

    # 🚫 Auto-delete Links
    app.add_handler(
        MessageHandler(
            filters.Entity("url") | filters.Entity("text_link"),
            auto_delete_links))

    # 💬 Auto-reply System
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_chat_messages))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
