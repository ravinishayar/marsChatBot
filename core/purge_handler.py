# core/purge.py

import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from telegram.error import TelegramError


async def purge_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ Please reply to a message before using /purge.")
        return

    chat_id = update.effective_chat.id
    from_msg_id = update.message.reply_to_message.message_id
    to_msg_id = update.message.message_id

    # Typing animation
    await context.bot.send_chat_action(chat_id=chat_id,
                                       action=ChatAction.TYPING)

    # Prepare deletion tasks
    delete_tasks = []
    for msg_id in range(from_msg_id, to_msg_id + 1):
        delete_tasks.append(
            context.bot.delete_message(chat_id=chat_id, message_id=msg_id))

    # Run deletions in parallel (faster)
    results = await asyncio.gather(*delete_tasks, return_exceptions=True)
    deleted = sum(1 for r in results if not isinstance(r, Exception))

    # Send confirmation message (auto-delete after 3 seconds)
    try:
        confirm = await context.bot.send_message(
            chat_id=chat_id,
            text=f"✅ MARS: Successfully deleted {deleted} messages.",
            disable_notification=True)
        await asyncio.sleep(3)
        await confirm.delete()
    except TelegramError:
        pass
