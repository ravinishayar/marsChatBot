from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from rapidfuzz import fuzz
import emoji
from telegram import Update
from telegram.ext import ContextTypes

conversations = {}

SIMILARITY_THRESHOLD = 70


# 🔤 Step 1: Normalize Hindi (Devanagari) to Roman Hindi
def normalize_message(msg: str) -> str:
    msg = msg.strip().lower()
    contains_hindi = any('\u0900' <= ch <= '\u097F' for ch in msg)
    if contains_hindi:
        try:
            msg = transliterate(msg, sanscript.DEVANAGARI,
                                sanscript.ITRANS).lower()
        except:
            pass
    return msg


# 🎯 Main reply function
def get_reply(user_msg: str) -> str:
    msg = user_msg.strip()

    # ✅ Case 1: Only emojis
    only_emojis = all(char in emoji.EMOJI_DATA
                      for char in msg) and not any(c.isalnum() for c in msg)
    if only_emojis:
        for char in msg:
            if char in emoji_responses:
                return emoji_responses[char]
        return None  # unknown emoji, stay silent

    # ✅ Case 2: Text + emoji
    first_emoji = next((char for char in msg if char in emoji.EMOJI_DATA),
                       None)
    text_only = ''.join(char for char in msg
                        if char not in emoji.EMOJI_DATA).strip()

    # 🔤 Normalize to Roman Hindi
    text_normalized = normalize_message(text_only)

    # ✅ Case 3: Exact match
    if text_normalized in conversations:
        return conversations[text_normalized] + (f" {first_emoji}"
                                                 if first_emoji else "")

    # ✅ Case 4: Fuzzy match
    best_match = None
    highest_score = 0
    for key in conversations:
        score = fuzz.ratio(text_normalized, key)
        if score > highest_score:
            highest_score = score
            best_match = key

    if highest_score >= SIMILARITY_THRESHOLD:
        return conversations[best_match] + (f" {first_emoji}"
                                            if first_emoji else "")

    # ❌ No match found: stay silent
    return None


# 🚀 Telegram message handler
async def handle_chat_messages(update: Update,
                               context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    reply = get_reply(user_msg)

    if reply:
        await update.message.reply_text(reply)
    else:
        pass  # stay silent


from telegram import Update
from telegram.ext import ContextTypes
import os

LOGGER_GROUP_ID = os.getenv("LOGGER_GROUP_ID")  # Set this in Replit secrets


async def handle_chat_messages(update: Update,
                               context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    user_msg = update.message.text
    reply = get_reply(user_msg)

    # ✅ 1. Log user message to LOGGER group
    try:
        log_text = (
            f"💬 <b>New Message</b>\n"
            f"👤 Name: {user.full_name}\n"
            f"🔗 Username: @{user.username if user.username else 'N/A'}\n"
            f"🆔 User ID: <code>{user.id}</code>\n"
            f"💭 Message: <code>{user_msg}</code>\n"
            f"📍 Chat: {chat.title if chat.title else 'Private Chat'}")
        await context.bot.send_message(chat_id=int(LOGGER_GROUP_ID),
                                       text=log_text,
                                       parse_mode="HTML")
    except Exception as e:
        print(f"❌ Failed to log message: {e}")

    # ✅ 2. Reply to the user
    if reply and reply != "none":
        await update.message.reply_text(reply)
