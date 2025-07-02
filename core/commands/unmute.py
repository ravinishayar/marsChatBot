from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes


async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ कृपया जिस यूज़र को unmute करना है, उसके मैसेज को reply करें।")
        return

    user_to_unmute = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id

    try:
        # ✅ सभी message permissions allow करें (basic)
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_to_unmute.id,
            permissions=ChatPermissions(can_send_messages=True))
        await update.message.reply_text(
            f"🔊 {user_to_unmute.mention_html()} को unmute कर दिया गया है।",
            parse_mode="HTML")
    except Exception as e:
        await update.message.reply_text(f"❌ Unmute नहीं किया जा सका: {e}")
