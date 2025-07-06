# core/broadcast.py
import json
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from core.broadcast_utils import load_users, load_groups


# ✅ Broadcast to all users
async def user_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        message_to_send = update.message.reply_to_message.text
    elif context.args:
        message_to_send = " ".join(context.args)
    else:
        await update.message.reply_text(
            "⚠️ Usage: /broadcast <your message> or reply to a message.")
        return

    users = load_users()
    success = 0
    failed = 0

    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id,
                                           text=message_to_send)
            success += 1
        except Exception as e:
            print(f"❌ Failed to send to {user_id}: {e}")
            failed += 1

    await update.message.reply_text(
        f"✅ User Broadcast completed.\n📬 Delivered: {success}\n❌ Failed: {failed}"
    )


# ✅ Broadcast to all groups
async def group_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        message_to_send = update.message.reply_to_message.text
    elif context.args:
        message_to_send = " ".join(context.args)
    else:
        await update.message.reply_text(
            "⚠️ Usage: /groupbroadcast <your message> or reply to a message.")
        return

    groups = load_groups()
    success = 0
    failed = 0

    for group_id in groups:
        try:
            await context.bot.send_message(chat_id=group_id,
                                           text=message_to_send)
            success += 1
        except Exception as e:
            print(f"❌ Failed to send to {group_id}: {e}")
            failed += 1

    await update.message.reply_text(
        f"✅ Group Broadcast completed.\n📬 Delivered: {success}\n❌ Failed: {failed}"
    )


# ✅ Return Handlers for main.py
def get_broadcast_handlers():
    return [
        CommandHandler("broadcast", user_broadcast),
        CommandHandler("groupbroadcast", group_broadcast),
    ]
