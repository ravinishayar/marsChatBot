import json
import os
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

BROADCAST_LOG = "broadcast_users.json"


def get_users():
    if os.path.exists(BROADCAST_LOG):
        with open(BROADCAST_LOG, "r") as f:
            return json.load(f)
    return []


async def broadcast_command(update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("ℹ️ Usage: /broadcast <your message>")
        return

    message = " ".join(context.args)
    users = get_users()

    success = 0
    fail = 0

    for user_id in users:
        try:
            print(f"📤 Sending to {user_id}")
            await context.bot.send_message(
                chat_id=int(user_id),
                text=message,
                parse_mode="HTML"  # You can change to Markdown if needed
            )
            success += 1
        except Exception as e:
            print(f"❌ Failed to send to {user_id}: {e}")
            fail += 1

    await update.message.reply_text(f"✅ Broadcast completed.\n"
                                    f"📬 Delivered: {success}\n"
                                    f"❌ Failed: {fail}")


def get_broadcast_handler():
    return CommandHandler("broadcast", broadcast_command)
