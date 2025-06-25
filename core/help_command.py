from telegram import Update
from telegram.ext import ContextTypes


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🛠 <b>Commands List</b>\n\n"
        "👤 <b>For Users:</b>\n"
        "• /start - बॉट शुरू करें\n"
        "• /help - यह सहायता मेनू\n\n"
        "👮 <b>For Admins:</b>\n"
        "• /setwelcome - वेलकम मैसेज सेट करें\n"
        "• /warn - यूज़र को चेतावनी दें\n"
        "• /broadcast - सभी यूज़र्स को ब्रॉडकास्ट भेजें\n"
        "• /broadcast_groups - सभी ग्रुप्स को ब्रॉडकास्ट भेजें\n\n"
        "🔗 Link Protection और ⚠️ Warning सिस्टम बॉट में ऑटोमेटिक काम करता है।\n\n"
        "❓ किसी भी दिक्कत के लिए @ravinishayar54 से संपर्क करें।")
    await update.message.reply_text(text, parse_mode="HTML")
