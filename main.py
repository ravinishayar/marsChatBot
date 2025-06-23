import os
import re
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler,
                          CallbackQueryHandler, ContextTypes, filters,
                          ChatMemberHandler)

from buttons import get_start_buttons, handle_button_click
from responses import get_reply
from start_handler import start
from welcome import set_welcome_start, save_welcome_message, welcome_new_member
from warnsystem import get_warn_handler
from user_logger import forward_user_message  # ✅ User message logger
from group_join_handler import welcome_on_add  # ✅ New group add handler

# 🔐 Get bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")


# /id command
async def send_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"🆔 Chat ID: `{chat_id}`",
                                    parse_mode="Markdown")


# 🔗 Delete messages containing links (for groups)
async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text or ""
    url_pattern = r"(https?://|t\\.me/|wa\\.me/|youtu\\.be|youtube\\.com)"
    if re.search(url_pattern, text, re.IGNORECASE):
        try:
            await message.delete()
            print("🚫 Deleted a message with link")
            return True
        except Exception as e:
            print(f"❌ Could not delete message: {e}")
    return False


# 🔁 Universal message handler for all chat types
async def handle_all_messages(update: Update,
                              context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type
    text = update.message.text

    if not text:
        return

    # ✅ Log private messages
    if chat_type == "private":
        await forward_user_message(update, context)

    # ✅ Save welcome message if in setup
    if context.user_data.get("setting_welcome"):
        await save_welcome_message(update, context)
        return

    # ✅ Link deletion in groups
    if chat_type in ["group", "supergroup"]:
        deleted = await delete_links(update, context)
        if deleted:
            return

    # 🤖 Auto-reply
    reply = get_reply(text)
    if reply:
        await update.message.reply_text(reply)


# 🔧 Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", send_chat_id))
    app.add_handler(CommandHandler("setwelcome", set_welcome_start))

    # Inline buttons
    app.add_handler(CallbackQueryHandler(handle_button_click))

    # Warning system
    app.add_handler(get_warn_handler())

    # Welcome new members
    app.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS,
                       welcome_new_member))

    # ✅ Bot added to group handler
    app.add_handler(
        ChatMemberHandler(welcome_on_add, ChatMemberHandler.MY_CHAT_MEMBER))

    # ✅ Universal message handler
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all_messages))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
