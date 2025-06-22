# warnsystem.py

import json
import os
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from collections import defaultdict

# JSON file to store warnings
WARN_FILE = "warns.json"

# Load warnings from file
def load_warnings():
    if os.path.exists(WARN_FILE):
        with open(WARN_FILE, "r") as f:
            return json.load(f)
    return {}

# Save warnings to file
def save_warnings(data):
    with open(WARN_FILE, "w") as f:
        json.dump(data, f)

warnings_data = load_warnings()

async def warn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ कृपया /warn का उपयोग किसी message के reply में करें।")
        return

    warned_user = update.message.reply_to_message.from_user
    chat_id = str(update.effective_chat.id)
    user_id = str(warned_user.id)

    warnings_data.setdefault(chat_id, {})
    warnings_data[chat_id][user_id] = warnings_data[chat_id].get(user_id, 0) + 1
    count = warnings_data[chat_id][user_id]

    save_warnings(warnings_data)

    if count >= 2:
        try:
            await context.bot.ban_chat_member(chat_id=int(chat_id), user_id=int(user_id))
            await update.message.reply_text(
                f"🚫 {warned_user.mention_html()} को 2 warnings के बाद banned कर दिया गया।",
                parse_mode="HTML"
            )
            warnings_data[chat_id].pop(user_id)
            save_warnings(warnings_data)
        except Exception as e:
            await update.message.reply_text(f"❌ Ban error: {e}")
    else:
        await update.message.reply_text(
            f"⚠️ {warned_user.mention_html()} को warning दी गई है। कुल warnings: {count}/2",
            parse_mode="HTML"
        )

def get_warn_handler():
    return CommandHandler("warn", warn_user)
