from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


def get_start_buttons():
    keyboard = [
        [
            InlineKeyboardButton(
                "➕ Add me to your group",
                url="https://t.me/GroupHelpManage0bot?startgroup=true")
        ], [InlineKeyboardButton("💡 Help", callback_data='help')],
        [
            InlineKeyboardButton("👥 Support Group",
                                 url="https://t.me/MARS_MACHAL_SUPPORT")
        ],
        [InlineKeyboardButton("👑 Owner", url="https://t.me/ravinishayar54")]
    ]
    return InlineKeyboardMarkup(keyboard)


# ✅ Required for main.py to import
async def handle_button_click(update: Update,
                              context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        try:
            if query.message.text:
                await query.edit_message_text(
                    "🛠 Help section: Ask me anything!")
            else:
                await query.message.reply_text(
                    "🛠 Help section: Ask me anything!")
        except Exception as e:
            print("❌ Error in button click:", e)


print("✅ buttons.py loaded")
