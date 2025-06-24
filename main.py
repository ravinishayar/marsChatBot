from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler,
                          CallbackQueryHandler, ChatMemberHandler, filters)
import os

# 🔁 logic from core
from core import (start, handle_button_click, set_welcome_start,
                  save_welcome_message, welcome_new_member, welcome_on_add,
                  handle_chat_messages)
from core.warnsystem import get_warn_handler  # ✅ Warning system
from core.link_protection import auto_delete_links  # ✅ Link delete system

BOT_TOKEN = os.getenv("BOT_TOKEN")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # 🟢 Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setwelcome", set_welcome_start))
    app.add_handler(get_warn_handler())  # ✅ /warn handler

    # 🔘 Inline button callback
    app.add_handler(CallbackQueryHandler(handle_button_click))

    # 🙋 Welcome new members
    app.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS,
                       welcome_new_member))

    # 📌 When bot is added to group
    app.add_handler(
        ChatMemberHandler(welcome_on_add, ChatMemberHandler.MY_CHAT_MEMBER))

    # 🚫 Auto-delete link messages (even from bots)
    app.add_handler(
        MessageHandler(
            filters.Entity("url") | filters.Entity("text_link"),
            auto_delete_links))

    # 💬 All text messages (except commands)
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_chat_messages))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
