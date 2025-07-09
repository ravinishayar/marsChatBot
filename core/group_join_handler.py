from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import Forbidden
from core.broadcast_utils import save_user_if_not_exists

# 🌐 भाषा सेटिंग स्टोर
group_languages = {}  # {chat_id: 'hi'/'en'}


# 👥 जब नया सदस्य group में आता है
async def welcome_new_member(update: Update,
                             context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            continue  # Bot खुद को welcome न करे

        try:
            await update.message.reply_text(f"👋 स्वागत है, {member.full_name}!"
                                            )
        except Exception as e:
            print(f"[❌] Error welcoming user: {e}")

    try:
        chat_id = update.effective_chat.id
        save_user_if_not_exists(chat_id)
    except Exception as e:
        print(f"[❌] Error saving group ID: {e}")


# 🤖 जब बॉट को group में manually जोड़ा जाता है
async def welcome_on_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = update.my_chat_member
    if status.new_chat_member.status in ["member", "administrator"]:
        chat_id = update.effective_chat.id
        chat_title = update.effective_chat.title

        # ✅ 1. Send Subscribe Message
        subscribe_keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("📢 Subscribe Channel",
                                 url="https://t.me/GroupHelpChatGuard")
        ]])

        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text="📢 <b>Support us by subscribing to our channel!</b>",
                reply_markup=subscribe_keyboard,
                parse_mode="HTML")
        except Forbidden:
            print(f"[⚠️] Bot removed from group: {chat_title} ({chat_id})")
            return
        except Exception as e:
            print(f"[❌] Error sending subscribe message: {e}")

        # ✅ 2. Send Permissions & Language Options
        language_keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("🌐 Change Language",
                                 callback_data=f"change_language|{chat_id}")
        ]])

        permissions_text = (
            f"👋 Thanks for adding <b>Group Help Bot</b> to <b>{chat_title}</b>!\n\n"
            "🛡️ This Ultra Group Manager bot will automatically help you manage your group.\n\n"
            "<b>Required Permissions:</b>\n"
            "• Delete messages\n"
            "• Ban users\n"
            "• Manage Stories\n"
            "• Invite Users via Link\n\n"
            "👇 Use the button below to change language:")

        try:
            await context.bot.send_message(chat_id=chat_id,
                                           text=permissions_text,
                                           reply_markup=language_keyboard,
                                           parse_mode="HTML")
        except Forbidden:
            print(f"[⚠️] Bot removed from group: {chat_title} ({chat_id})")
            return
        except Exception as e:
            print(f"[❌] Error sending permissions message: {e}")

        try:
            save_user_if_not_exists(chat_id)
        except Exception as e:
            print(f"[❌] Error saving group ID: {e}")


# 🌐 जब user "Change Language" पर क्लिक करे
async def change_language_callback(update: Update,
                                   context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = int(query.data.split("|")[1])

    language_buttons = InlineKeyboardMarkup([[
        InlineKeyboardButton("🇮🇳 Hindi",
                             callback_data=f"set_lang|hi|{chat_id}"),
        InlineKeyboardButton("🇬🇧 English",
                             callback_data=f"set_lang|en|{chat_id}")
    ]])

    try:
        await query.edit_message_text(text="🌐 Select a language / भाषा चुनें:",
                                      reply_markup=language_buttons)
    except Exception as e:
        print(f"[❌] Error showing language options: {e}")


# ✅ जब user Hindi/English चुने
async def set_language_callback(update: Update,
                                context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, lang, chat_id = query.data.split("|")
    chat_id = int(chat_id)

    group_languages[chat_id] = lang

    if lang == "hi":
        msg = ("✅ भाषा हिंदी में सेट हो गई है!\n\n"
               "अब से सभी मैसेज हिंदी में आएंगे।")
    else:
        msg = ("✅ Language has been set to English!\n\n"
               "All future messages will be in English.")

    try:
        await query.edit_message_text(msg)
    except Exception as e:
        print(f"[❌] Error setting language: {e}")
