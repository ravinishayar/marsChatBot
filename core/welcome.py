from telegram import Update
from telegram.ext import ContextTypes


# ✅ Step 1: Admin sets a welcome message
async def set_welcome_start(update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✏️ कृपया वह वेलकम मैसेज भेजिए जिसे आप सेट करना चाहते हैं।\n\n"
        "🔁 आप {user} और {group} का इस्तेमाल कर सकते हैं।")
    context.user_data["setting_welcome"] = True


# ✅ Step 2: Save welcome message to file
async def save_welcome_message(update: Update,
                               context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("setting_welcome"):
        welcome_text = update.message.text
        with open("welcome_message.txt", "w", encoding="utf-8") as f:
            f.write(welcome_text)
        await update.message.reply_text("✅ Welcome message सेव हो गया!")
        context.user_data["setting_welcome"] = False


# ✅ Step 3: Send welcome message to new members (excluding bot itself)
async def welcome_new_member(update: Update,
                             context: ContextTypes.DEFAULT_TYPE):
    # Read saved welcome message
    try:
        with open("welcome_message.txt", "r", encoding="utf-8") as f:
            welcome_text = f.read()
    except FileNotFoundError:
        welcome_text = "👋 नमस्ते {user}, आपका {group} में स्वागत है!"

    bot_id = context.bot.id

    for member in update.message.new_chat_members:
        if member.id == bot_id:
            continue  # ⛔ Don't welcome the bot itself

        personalized_message = welcome_text.format(
            user=member.mention_html(),
            group=update.effective_chat.title or "हमारे ग्रुप")

        await update.message.reply_text(
            personalized_message,
            parse_mode="HTML"  # ✅ No buttons
        )
