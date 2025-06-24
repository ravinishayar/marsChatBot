import os
from telegram import Update
from telegram.ext import ContextTypes
from core.inline_buttons import get_start_buttons

BOT_TOKEN = os.getenv("BOT_TOKEN")
LOGGER_GROUP_ID = os.getenv("LOGGER_GROUP_ID")  # Add in Secrets or .env


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_url = "https://files.catbox.moe/tinlr0.jpg"
    caption = (
        "👋 <b>नमस्ते!</b> मैं आपका Auto Reply Bot हूँ।\n"
        "🤖 मुझसे बात करें और मैं आपको जवाब दूँगा।\n\n"
        "👇 नीचे के बटन से मुझे अपने ग्रुप में जोड़ें:"
    )

    # 1. Send image + caption with inline buttons
    await update.message.reply_photo(
        photo=image_url,
        caption=caption,
        reply_markup=get_start_buttons(),
        parse_mode="HTML"
    )

    # 2. Log user info to LOGGER group (if set)
    user = update.effective_user
    if LOGGER_GROUP_ID:
        log_msg = (
            f"🚀 <b>New /start</b>\n"
            f"👤 Name: {user.full_name}\n"
            f"🔗 Username: @{user.username if user.username else 'N/A'}\n"
            f"🆔 User ID: <code>{user.id}</code>"
        )
        try:
            await context.bot.send_message(
                chat_id=int(LOGGER_GROUP_ID),
                text=log_msg,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"❌ Logger error: {e}")
