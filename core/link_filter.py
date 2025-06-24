import re
from telegram import Update
from telegram.ext import ContextTypes

# 🔗 Regex to detect URLs
LINK_PATTERN = re.compile(r'https?://\S+|www\.\S+')

async def auto_delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        if re.search(LINK_PATTERN, update.message.text):
            try:
                await update.message.delete()
                print("🔗 Link deleted!")
            except Exception as e:
                print(f"❌ Error deleting link: {e}")
