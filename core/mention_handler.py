from telegram import Update
from telegram.ext import ContextTypes
import asyncio

# ✅ Track active mentions
active_mentions = []

async def mention_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    # ✅ Check if command is in a group
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("❌ यह कमांड केवल ग्रुप में उपयोग की जा सकती है।")
        return

    # ✅ Check if user is admin
    member = await context.bot.get_chat_member(chat.id, user.id)
    if member.status not in ["administrator", "creator"]:
        await update.message.reply_text("❌ केवल एडमिन ही सभी को टैग कर सकते हैं।")
        return

    # ✅ Determine message mode
    if context.args and update.message.reply_to_message:
        await update.message.reply_text("⚠️ एक बार में केवल एक आर्ग्यूमेंट दें।")
        return
    elif context.args:
        mode = "text_on_cmd"
        custom_text = " ".join(context.args)
    elif update.message.reply_to_message:
        mode = "text_on_reply"
        reply_msg = update.message.reply_to_message
        custom_text = None
    else:
        await update.message.reply_text("⚠️ कृपया reply करें या `/mentionall <संदेश>` लिखें।")
        return

    # ✅ Start mention process
    active_mentions.append(chat.id)
    mentions = []
    count = 0

    try:
        total_members = await context.bot.get_chat_member_count(chat.id)

        for user_id in range(1, total_members + 1):
            if chat.id not in active_mentions:
                break  # Stop if /cancel is called

            try:
                member = await context.bot.get_chat_member(chat.id, user_id)
            except:
                continue  # Skip invalid users

            if member.user.is_bot:
                continue

            count += 1
            mentions.append(f"[{member.user.first_name}](tg://user?id={member.user.id})")

            if count % 5 == 0:
                text = " ".join(mentions)
                if mode == "text_on_cmd":
                    text += f"\n\n{custom_text}"
                    await context.bot.send_message(chat.id, text, parse_mode="Markdown")
                elif mode == "text_on_reply":
                    await reply_msg.reply_text(text, parse_mode="Markdown")
                mentions = []
                await asyncio.sleep(2)

        # ✅ Send any remaining mentions
        if mentions:
            text = " ".join(mentions)
            if mode == "text_on_cmd":
                text += f"\n\n{custom_text}"
                await context.bot.send_message(chat.id, text, parse_mode="Markdown")
            elif mode == "text_on_reply":
                await reply_msg.reply_text(text, parse_mode="Markdown")

    except Exception as e:
        print(f"Error: {e}")

    try:
        active_mentions.remove(chat.id)
    except:
        pass


async def cancel_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.id in active_mentions:
        active_mentions.remove(chat.id)
        await update.message.reply_text("✅ टैगिंग प्रोसेस रोक दी गई।")
    else:
        await update.message.reply_text("ℹ️ इस समय कोई टैगिंग प्रोसेस नहीं चल रही।")
