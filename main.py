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
    handle_button_click,
    set_welcome_start,
    save_welcome_message,
    welcome_new_member,
    welcome_on_add,
    handle_chat_messages,
)
from core.warnsystem import get_warn_handler  # ⚠️ Warning system
from core.link_protection import auto_delete_links  # 🔗 Link deletion
from core.broadcast import broadcast_command  # 📢 Broadcast to users
from core.group_broadcast import broadcast_groups, get_group_broadcast_handler  # 📢 Broadcast to groups

# 🔐 Bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ✅ Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setwelcome", set_welcome_start))
    app.add_handler(get_warn_handler())  # /warn
    app.add_handler(CommandHandler("broadcast", broadcast_command))  # Users
    app.add_handler(get_group_broadcast_handler())  # Groups

    # 🔘 Inline Button Callback
    app.add_handler(CallbackQueryHandler(handle_button_click))

    # 👥 Welcome & Bot Join
    app.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS,
                       welcome_new_member))
    app.add_handler(
        ChatMemberHandler(welcome_on_add, ChatMemberHandler.MY_CHAT_MEMBER))

    # 🚫 Auto-delete messages with links
    app.add_handler(
        MessageHandler(
            filters.Entity("url") | filters.Entity("text_link"),
            auto_delete_links))

    # 💬 Auto reply
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_chat_messages))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
