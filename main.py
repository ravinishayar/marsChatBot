import os
import asyncio
from dotenv import load_dotenv

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

# 🔐 Load env early
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 🔁 Import after env loaded
from core import (
    start,
    handle_chat_messages,
    welcome_new_member,
    welcome_on_add,
    help_command,
    handle_button_click,
)

# 🧹 Import others
from core.commands.info_command import info_command
from core.stats_handler import stats_handler
from core.broadcast import broadcast_command
from core.group_broadcast import get_group_broadcast_handler
from core.ban_handler import ban_user, unban_user
from core.commands.mute import mute_user
from core.commands.unmute import unmute_user
from core.commands.reload import reload_admins
from core.link_protection import auto_delete_links
from core.cleaner import auto_delete_media_task, register_group, store_media_message
from core.user_tracker import track_user
from core.warnsystem import get_warn_handler


async def register_chat(update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]:
        register_group(update.effective_chat.id)
    await handle_chat_messages(update, context)


async def track_media(update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]:
        register_group(update.effective_chat.id)
        if update.message and (update.message.photo or update.message.video
                               or update.message.document
                               or update.message.sticker):
            store_media_message(update.message)


async def main():
    print("🚀 Starting bot...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # 📆 Auto media deletion
    scheduler = AsyncIOScheduler()
    scheduler.add_job(auto_delete_media_task,
                      "interval",
                      minutes=2,
                      args=[app.bot])
    scheduler.start()

    # Handlers
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("unban", unban_user))
    app.add_handler(CommandHandler("mute", mute_user))
    app.add_handler(CommandHandler("unmute", unmute_user))
    app.add_handler(CommandHandler("reload", reload_admins))
    app.add_handler(stats_handler)

    app.add_handler(get_warn_handler())
    app.add_handler(get_group_broadcast_handler())
    app.add_handler(CallbackQueryHandler(handle_button_click))
    app.add_handler(MessageHandler(filters.ALL, track_user), group=-1)
    app.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS,
                       welcome_new_member))
    app.add_handler(
        ChatMemberHandler(welcome_on_add, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(
        MessageHandler(
            filters.Entity("url") | filters.Entity("text_link"),
            auto_delete_links))
    app.add_handler(
        MessageHandler(
            filters.PHOTO | filters.VIDEO | filters.Document.ALL
            | filters.Sticker.ALL, track_media))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, register_chat))

    print("🤖 Bot is running...")
    await app.run_polling()


if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
