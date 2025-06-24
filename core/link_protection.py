from telegram import Update
from telegram.ext import ContextTypes


async def auto_delete_links(update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.delete()
        print(f"🧹 Deleted link from user: {update.effective_user.id}")
    except Exception as e:
        print(f"❌ Failed to delete message: {e}")
