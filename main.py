import os
import asyncio
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ChatMemberHandler,
    ContextTypes,
    filters,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 🔁 Core Features
from core import (
    start,
    handle_chat_messages,
    set_welcome_start,
    save_welcome_message,
    welcome_new_member,
    welcome_on_add,
)
from core.purge_handler import purge_messages
from core.help_command import help_command
from core.inline_buttons import handle_button_click
from core.warnsystem import get_warn_handler
from core.link_protection import auto_delete_links
from core.broadcast import broadcast_command
from core.group_broadcast import broadcast_groups, get_group_broadcast_handler
from core.ban_handler import ban_user, unban_user
from core.moderation import mute_user, kick_user

# 🧹 Media Cleaner System
from core.cleaner import auto_delete_media_task, register_group, store_media_message

BOT_TOKEN = os.getenv("BOT_TOKEN")


# ✅ Register group for features like cleaner & auto-reply
async def register_chat(update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat and update.effective_chat.type in [
            "group", "supergroup"
    ]:
        register_group(update.effective_chat.id)
    await handle_chat_messages(update, context)


# 🖼️ Track photos/videos/stickers/documents
async def track_media(update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat and update.effective_chat.type in [
            "group", "supergroup"
    ]:
        register_group(update.effective_chat.id)
        if update.message and (update.message.photo or update.message.video
                               or update.message.document
                               or update.message.sticker):
            store_media_message(update.message)


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ⏱️ Auto-delete old media every 2 minutes
    scheduler = AsyncIOScheduler()
    scheduler.add_job(auto_delete_media_task,
                      "interval",
                      minutes=2,
                      args=[app.bot])
    scheduler.start()

    # 📋 Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("setwelcome", set_welcome_start))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("purge", purge_messages))
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("unban", unban_user))
    app.add_handler(CommandHandler("mute", mute_user))
    app.add_handler(CommandHandler("kick", kick_user))

    # ⚙️ Extra Features
    app.add_handler(get_warn_handler())
    app.add_handler(get_group_broadcast_handler())
    app.add_handler(CallbackQueryHandler(handle_button_click))

    # 👥 New Member Handlers
    app.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS,
                       welcome_new_member))
    app.add_handler(
        ChatMemberHandler(welcome_on_add, ChatMemberHandler.MY_CHAT_MEMBER))

    # 🔗 Auto-delete links
    app.add_handler(
        MessageHandler(
            filters.Entity("url") | filters.Entity("text_link"),
            auto_delete_links))

    # 📸 Media tracking (photo, video, document, sticker)
    app.add_handler(
        MessageHandler(
            filters.PHOTO | filters.VIDEO | filters.Document.ALL
            | filters.Sticker.ALL, track_media))

    # 🧠 Auto-reply & group register
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, register_chat))

    print("🤖 Bot is running...")
    await app.run_polling()


if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
