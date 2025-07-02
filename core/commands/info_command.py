from telegram import Update, User
from telegram.ext import ContextTypes
from html import escape


def get_user_info(user: User) -> str:
    first_name = escape(user.first_name or "")
    last_name = escape(user.last_name or "")
    username = f"@{user.username}" if user.username else "N/A"
    user_id = user.id
    is_bot = "Yes" if user.is_bot else "No"

    info = (
        f"<b>👤 User Info:</b>\n\n"
        f"<b>🆔 ID:</b> <code>{user_id}</code>\n"
        f"<b>📛 Name:</b> {first_name} {last_name}\n"
        f"<b>🔗 Username:</b> {username}\n"
        f"<b>🤖 Bot?</b> {is_bot}"
    )
    return info


# ✅ /info command handler
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Use replied user if present
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    else:
        user = update.effective_user

    info_text = get_user_info(user)

    await update.message.reply_text(
        text=info_text,
        parse_mode="HTML",
        disable_web_page_preview=True
    )
