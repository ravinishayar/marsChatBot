from telegram import Update
from telegram.ext import ContextTypes


# Step 1: Set welcome message manually (admin command)
async def set_welcome_start(update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✏️ कृपया वह वेलकम मैसेज भेजिए जिसे आप सेट करना चाहते हैं।\n\n🔁 आप {user} और {group} का इस्तेमाल कर सकते हैं।"
    )
    context.user_data["setting_welcome"] = True


# Step 2: Save welcome message sent by admin
async def save_welcome_message(update: Update,
                               context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("setting_welcome"):
        welcome_text = update.message.text
        with open("welcome_message.txt", "w", encoding="utf-8") as f:
            f.write(welcome_text)
        await update.message.reply_text("✅ Welcome message सेव हो गया!")
        context.user_data["setting_welcome"] = False


# Step 3: Welcome new users when they join
async def welcome_new_member(update: Update,
                             context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("welcome_message.txt", "r", encoding="utf-8") as f:
            welcome_text = f.read()
    except FileNotFoundError:
        # Default welcome message
        welcome_text = "👋 नमस्ते {user}, आपका {group} में स्वागत है!"

    for member in update.message.new_chat_members:
        personalized_message = welcome_text.format(
            user=member.mention_html(),
            group=update.effective_chat.title or "हमारे ग्रुप")
        await update.message.reply_text(personalized_message,
                                        parse_mode="HTML")
