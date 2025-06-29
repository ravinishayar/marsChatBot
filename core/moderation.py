from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes


# 🔇 /mute command
async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "किसी यूज़र के मैसेज पर reply करके /mute करें।")
        return

    user_id = update.message.reply_to_message.from_user.id
    try:
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False))
        await update.message.reply_text("🔇 यूज़र म्यूट कर दिया गया।")
    except Exception as e:
        await update.message.reply_text(f"❌ म्यूट नहीं हो सका: {e}")


# 👢 /kick command
async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "किसी यूज़र के मैसेज पर reply करके /kick करें।")
        return

    user_id = update.message.reply_to_message.from_user.id
    try:
        await context.bot.ban_chat_member(chat_id=update.effective_chat.id,
                                          user_id=user_id)
        await context.bot.unban_chat_member(  # optional unban to allow rejoining
            chat_id=update.effective_chat.id,
            user_id=user_id)
        await update.message.reply_text("👢 यूज़र को ग्रुप से निकाल दिया गया।")
    except Exception as e:
        await update.message.reply_text(f"❌ यूज़र को निकाल नहीं सके: {e}")
