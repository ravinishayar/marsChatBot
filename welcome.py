from telegram import Update
from telegram.ext import ContextTypes


# Step 1: Set welcome message
async def set_welcome_start(update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✏️ कृपया वह वेलकम मैसेज भेजिए जिसे आप सेट करना चाहते हैं।")
    context.user_data["setting_welcome"] = True


# Step 2: Save welcome message
async def save_welcome_message(update: Update,
                               context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("setting_welcome"):
        welcome_text = update.message.text
        with open("welcome_message.txt", "w", encoding="utf-8") as f:
            f.write(welcome_text)
        await update.message.reply_text("✅ Welcome message save हो गया!")
        context.user_data["setting_welcome"] = False


# Step 3: Send welcome when a user joins
async def welcome_new_member(update: Update,
                             context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("welcome_message.txt", "r", encoding="utf-8") as f:
            welcome_text = f.read()
    except FileNotFoundError:
        welcome_text = "👋 स्वागत है!"

    for member in update.message.new_chat_members:
        await update.message.reply_text(
            f"{member.mention_html()} {welcome_text}", parse_mode="HTML")
