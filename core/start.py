import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from telegram import Update
from telegram.ext import ContextTypes
from core.inline_buttons import get_start_buttons  # inline buttons system


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 🌐 Image from a URL
    image_url = "https://files.catbox.moe/tinlr0.jpg"  # <-- यहां अपनी image URL डालें

    # 1. Send the image via URL
    await update.message.reply_photo(photo=image_url)

    # 2. Send welcome text with buttons
    await update.message.reply_text(
        "👋 नमस्ते! मैं Auto Reply Bot हूँ।\n\n"
        "✨ मुझे ग्रुप में जोड़ें और मुझसे हिंदी में बात करें।\n"
        "🚫 किसी भी लिंक को ऑटो डिलीट कर सकता हूँ।\n"
        "🧠 OpenAI या Gemini API से जवाब देता हूँ।\n\n"
        "👇 नीचे दिए गए बटन से शुरू करें:",
        reply_markup=get_start_buttons())
