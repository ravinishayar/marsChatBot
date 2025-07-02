from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from pymongo import MongoClient
import os

# ✅ MongoDB Setup (MONGO_DB_URI used)
client = MongoClient(os.getenv("MONGO_DB_URI"))
db = client["bot"]
users = db["users"]


# ✅ BAN USER
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

    target_user = None

    # ✅ Case 1: Reply-based
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user

    # ✅ Case 2: Argument-based
    elif context.args:
        arg = context.args[0]
        try:
            if arg.startswith("@"):
                username = arg[1:]
                user_data = users.find_one({"username": username})
                if user_data:
                    target_user_id = user_data["user_id"]
                    await bot.ban_chat_member(chat.id, target_user_id)
                    await update.message.reply_text(
                        f"@{username} को बैन कर दिया गया ✅ (लोकल DB से खोजा गया)।"
                    )
                    return
                else:
                    await update.message.reply_text(
                        "⚠️ यूज़र नहीं मिला MongoDB में।")
                    return
            elif arg.isdigit():
                target_user = (await bot.get_chat_member(chat.id,
                                                         int(arg))).user
            else:
                await update.message.reply_text(
                    "❌ यूज़र आईडी/username सही नहीं है।")
                return
        except Exception as e:
            await update.message.reply_text(
                f"⚠️ Error: यूज़र नहीं मिला। {str(e)}")
            return

    if not target_user:
        await update.message.reply_text(
            "⚠️ कृपया reply करें या username/user ID दें।")
        return

    try:
        await bot.ban_chat_member(chat.id, target_user.id)
        await update.message.reply_text(
            f"{target_user.mention_html()} को बैन कर दिया गया है ✅",
            parse_mode="HTML")
    except BadRequest as e:
        await update.message.reply_text(f"बैन नहीं कर पाए ❌: {e.message}")


# ✅ UNBAN USER
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

    target_user = None

    # ✅ Case 1: If replied
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user

    # ✅ Case 2: Argument-based
    elif context.args:
        arg = context.args[0]
        try:
            if arg.startswith("@"):
                username = arg[1:]
                user_data = users.find_one({"username": username})
                if user_data:
                    target_user_id = user_data["user_id"]
                    await bot.unban_chat_member(chat.id, target_user_id)
                    await update.message.reply_text(
                        f"@{username} को अनबैन कर दिया गया ✅ (लोकल DB से)।")
                    return
                else:
                    await update.message.reply_text(
                        "⚠️ यूज़र MongoDB में नहीं मिला।")
                    return
            elif arg.isdigit():
                target_user = (await bot.get_chat_member(chat.id,
                                                         int(arg))).user
            else:
                await update.message.reply_text(
                    "❌ यूज़र ID/username सही नहीं है।")
                return
        except Exception as e:
            await update.message.reply_text(f"⚠️ Error: {str(e)}")
            return

    if not target_user:
        await update.message.reply_text(
            "⚠️ कृपया reply करें या username/user ID दें।")
        return

    try:
        await bot.unban_chat_member(chat.id, target_user.id)
        await update.message.reply_text(
            f"{target_user.mention_html()} को अनबैन कर दिया गया ✅",
            parse_mode="HTML")
    except BadRequest as e:
        await update.message.reply_text(f"अनबैन नहीं कर पाए ❌: {e.message}")
