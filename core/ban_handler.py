# core/ban_handler.py

from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.error import BadRequest


async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    chat = update.effective_chat
    user = update.effective_user
    bot = context.bot

    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text(
            "यह कमांड सिर्फ़ ग्रुप में काम करती है।")
        return

    member = await chat.get_member(user.id)
    if member.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await update.message.reply_text(
            "सिर्फ़ एडमिन ही किसी को बैन कर सकते हैं।")
        return

    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
    elif context.args:
        try:
            if context.args[0].startswith("@"):
                chat_member = await bot.get_chat_member(
                    chat.id, context.args[0])
                target_user = chat_member.user
            else:
                chat_member = await bot.get_chat_member(
                    chat.id, int(context.args[0]))
                target_user = chat_member.user
        except Exception:
            await update.message.reply_text(
                "यूज़र नहीं मिला। कृपया reply करें या user ID दें।")
            return
    else:
        await update.message.reply_text("कृपया reply करें या user ID दें।")
        return

    try:
        await bot.ban_chat_member(chat.id, target_user.id)
        await update.message.reply_text(
            f"{target_user.mention_html()} को बैन कर दिया गया है।",
            parse_mode="HTML")
    except BadRequest as e:
        await update.message.reply_text(f"बैन नहीं कर पाए: {e.message}")


async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    chat = update.effective_chat
    user = update.effective_user
    bot = context.bot

    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text(
            "यह कमांड सिर्फ़ ग्रुप में काम करती है।")
        return

    member = await chat.get_member(user.id)
    if member.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await update.message.reply_text(
            "सिर्फ़ एडमिन ही किसी को अनबैन कर सकते हैं।")
        return

    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
    elif context.args:
        try:
            if context.args[0].startswith("@"):
                chat_member = await bot.get_chat_member(
                    chat.id, context.args[0])
                target_user = chat_member.user
            else:
                chat_member = await bot.get_chat_member(
                    chat.id, int(context.args[0]))
                target_user = chat_member.user
        except Exception:
            await update.message.reply_text(
                "यूज़र नहीं मिला। कृपया reply करें या user ID दें।")
            return
    else:
        await update.message.reply_text("कृपया reply करें या user ID दें।")
        return

    try:
        await bot.unban_chat_member(chat.id, target_user.id)
        await update.message.reply_text(
            f"{target_user.mention_html()} को अनबैन कर दिया गया है।",
            parse_mode="HTML")
    except BadRequest as e:
        await update.message.reply_text(f"अनबैन नहीं कर पाए: {e.message}")
