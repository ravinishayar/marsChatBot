import os
import asyncio
import threading
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

# 🛡 Pyrogram for mention system
from pyrogram import Client as PyroClient, filters as pyro_filters
from core.mention_handler import (
    mention_all_pyro,
    mention_admins_pyro,
    cancel_mention_pyro,
)  # ✅ Pyrogram Mention System

# 🔐 Load .env variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# ✅ Import core handlers
from core import (
    start,
    handle_chat_messages,
    welcome_on_add,
    help_command,
    handle_button_click,
)
from core.welcome import set_welcome_start, welcome_new_member
from core.purge_handler import purge_messages
from core.commands.info_command import info_command
from core.stats_handler import stats_handler
from core.broadcast import get_broadcast_handlers
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


async def auto_register_on_admin(update, context: ContextTypes.DEFAULT_TYPE):
    if update.my_chat_member and update.my_chat_member.new_chat_member.status in [
            "administrator", "creator"
    ]:
        group_id = update.effective_chat.id
        group_title = update.effective_chat.title
        print(f"✅ Bot is admin in group: {group_title} ({group_id})")
        register_group(group_id)
        from core.broadcast_utils import save_group
        save_group(group_id, group_title)


async def on_startup(app):
    print("📆 Starting scheduler...")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(auto_delete_media_task,
                      "interval",
                      minutes=2,
                      args=[app.bot])
    scheduler.start()
    print("✅ Scheduler started")


def run_pyrogram():
    pyro_client = PyroClient(
        "mention_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
    )

    @pyro_client.on_message(
        pyro_filters.command("mentionall") & pyro_filters.group)
    async def handle_mention_all(client, message):
        await mention_all_pyro(client, message)

    @pyro_client.on_message(pyro_filters.command("admin") & pyro_filters.group)
    async def handle_mention_admins(client, message):
        await mention_admins_pyro(client, message)

    @pyro_client.on_message(
        pyro_filters.command("cancel") & pyro_filters.group)
    async def handle_cancel_mention(client, message):
        await cancel_mention_pyro(client, message)

    print("✅ Pyrogram mention system running...")
    pyro_client.run()


async def start_telegram_bot():
    print("🚀 Starting Telegram Bot...")
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(on_startup).build()

    # ✅ Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handlers(get_broadcast_handlers())
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("unban", unban_user))
    app.add_handler(CommandHandler("mute", mute_user))
    app.add_handler(CommandHandler("unmute", unmute_user))
    app.add_handler(CommandHandler("reload", reload_admins))
    app.add_handler(CommandHandler("setwelcome", set_welcome_start))
    app.add_handler(CommandHandler("purge", purge_messages))
    app.add_handler(stats_handler)
    app.add_handler(get_warn_handler())
    app.add_handler(CallbackQueryHandler(handle_button_click))
    app.add_handler(MessageHandler(filters.ALL, track_user), group=-1)
    app.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS,
                       welcome_new_member))
    app.add_handler(
        ChatMemberHandler(welcome_on_add, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(
        ChatMemberHandler(auto_register_on_admin,
                          ChatMemberHandler.MY_CHAT_MEMBER))
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

    print("✅ Telegram Bot is running...")
    await app.run_polling()


if __name__ == "__main__":
    # Run Pyrogram in a separate thread
    threading.Thread(target=run_pyrogram, daemon=True).start()

    # Start Telegram Bot in main thread's event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_telegram_bot())
