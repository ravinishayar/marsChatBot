# core/commands/mute.py

from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes


async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ कृपया जिस यूज़र को mute करना है, उसके मैसेज को reply करें।")
        return

    user_to_mute = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id

    try:
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_to_mute.id,
            permissions=ChatPermissions(can_send_messages=False))
        await update.message.reply_text(
            f"🔇 {user_to_mute.mention_html()} को mute कर दिया गया है।",
            parse_mode="HTML")
    except Exception as e:
        await update.message.reply_text(f"❌ Mute नहीं किया जा सका: {e}")
