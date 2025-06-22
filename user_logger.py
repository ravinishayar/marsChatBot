import os
from telegram import Update
from telegram.ext import ContextTypes

# CONFIG से LOG_GROUP_ID लें
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "-1002533639590"))  # fallback if not using .env

async def forward_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    user = update.effective_user

    # सिर्फ प्राइवेट चैट के लिए
    if update.effective_chat.type != "private":
        return

    if message.text:
        log_text = (
            f"📨 <b>New Message from:</b> {user.mention_html()}\n"
            f"🆔 <b>User ID:</b> <code>{user.id}</code>\n\n"
            f"💬 <b>Message:</b>\n<code>{message.text}</code>"
        )
        try:
            await context.bot.send_message(
                chat_id=LOG_GROUP_ID,
                text=log_text,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"❌ Failed to forward message: {e}")
