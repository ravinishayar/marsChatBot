# core/group_broadcast.py

import json
import os
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

GROUP_LOG = "broadcast_groups.json"


# 🔁 ग्रुप्स लोड करें
def get_groups():
    if os.path.exists(GROUP_LOG):
        with open(GROUP_LOG, "r") as f:
            return json.load(f)
    return []


# 📢 मैसेज भेजें सभी ग्रुप्स को
async def broadcast_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "📢 इस्तेमाल करें: /broadcast_groups <आपका मैसेज>")
        return

    message = " ".join(context.args)
    groups = get_groups()
    success, fail = 0, 0

    for group_id in groups:
        try:
            await context.bot.send_message(chat_id=group_id, text=message)
            success += 1
        except Exception:
            fail += 1

    await update.message.reply_text(
        f"✅ ग्रुप ब्रॉडकास्ट पूरा हुआ\n📤 भेजा गया: {success}\n❌ फेल हुए: {fail}"
    )


# ✅ Handler function
def get_group_broadcast_handler():
    return CommandHandler("broadcast_groups", broadcast_groups)
