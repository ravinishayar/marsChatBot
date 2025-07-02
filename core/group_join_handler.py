from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.broadcast_utils import save_user


# 👥 जब नया सदस्य group में आता है
async def welcome_new_member(update: Update,
                             context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        # ⛔ Skip if the new member is the bot itself
        if member.id == context.bot.id:
            continue

        try:
            await update.message.reply_text(f"👋 स्वागत है, {member.full_name}!"
                                            )
        except Exception as e:
            print(f"[❌] Error in user welcome: {e}")

    try:
        save_user(update.effective_chat.id)
    except Exception as e:
        print(f"[❌] Error saving group: {e}")


# 🤖 जब बॉट को group में manually जोड़ा जाता है
async def welcome_on_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = update.my_chat_member
    if status.new_chat_member.status in ["member", "administrator"]:
        chat_id = update.effective_chat.id
        chat_title = update.effective_chat.title

        # ✅ 1. Subscribe Message with Button
        subscribe_keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("📢 Subscribe Channel",
                                 url="https://t.me/YourChannelUsername")
        ]])

        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text="📢 <b>Support us by subscribing to our channel!</b>",
                reply_markup=subscribe_keyboard,
                parse_mode="HTML")
        except Exception as e:
            print(f"[❌] Error sending subscribe message: {e}")

        # ✅ 2. Settings Message with Options
        settings_keyboard = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("🛠️ Open Here",
                                     callback_data="open_settings_here")
            ],
             [
                 InlineKeyboardButton(
                     "🔐 Open in Private",
                     url=f"https://t.me/{context.bot.username}?start=settings")
             ]])

        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=(f"👋 Thanks for adding me to <b>{chat_title}</b>!\n\n"
                      "⚙️ Configure me using the buttons below:"),
                reply_markup=settings_keyboard,
                parse_mode="HTML")
        except Exception as e:
            print(f"[❌] Error sending settings message: {e}")

        try:
            save_user(chat_id)
        except Exception as e:
            print(f"[❌] Error saving group ID: {e}")
