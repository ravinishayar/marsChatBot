from telegram import Update
from telegram.ext import ContextTypes
from core.inline_buttons import get_start_buttons


async def welcome_new_member(update: Update,
                             context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"👋 स्वागत है, {member.full_name}!",
                                        reply_markup=get_start_buttons())


async def welcome_on_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = update.my_chat_member
    if status.new_chat_member.status in ["member", "administrator"]:
        chat_title = update.effective_chat.title
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(f"🚀 मुझे ग्रुप *{chat_title}* में जोड़ने के लिए धन्यवाद!\n\n"
                  "मैं एक ऑटो-रिप्लाई, वॉर्निंग और वेलकम मैसेज बोट हूँ।\n"
                  "नीचे दिए गए बटन से मेरी सुविधाएँ देखें:"),
            reply_markup=get_start_buttons(),
            parse_mode="Markdown")
