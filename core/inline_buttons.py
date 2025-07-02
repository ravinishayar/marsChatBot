from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from core.start import get_welcome_message

USER_LANGUAGES = {}


# 🔘 START MENU BUTTONS
def get_start_buttons():
    keyboard = [
        [
            InlineKeyboardButton(
                "➕ Add me to a Group",
                url="https://t.me/ChatManageHelpbot?startgroup=true")
        ],
        [
            InlineKeyboardButton("👥 Group",
                                 url="https://t.me/GroupHelpChatGuard"),
            InlineKeyboardButton("📢 Channel",
                                 url="https://t.me/GroupHelpChatGuard")
        ],
        [
            InlineKeyboardButton("💬 Support",
                                 url="https://t.me/GroupHelpChatGuard"),
            InlineKeyboardButton("ℹ️ Information", callback_data="info")
        ],
        [
            InlineKeyboardButton("🌐 🇮🇳 Languages",
                                 callback_data="language_menu")
        ], [InlineKeyboardButton("🛠 /help", callback_data="help_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)


# 🔘 LANGUAGE BUTTONS
def get_language_buttons():
    keyboard = [[
        InlineKeyboardButton("🇮🇳 Hindi", callback_data="lang_hi"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
    ],
                [
                    InlineKeyboardButton("🇵🇰 Urdu", callback_data="lang_ur"),
                    InlineKeyboardButton("🇧🇩 Bengali", callback_data="lang_bn")
                ],
                [
                    InlineKeyboardButton("🇮🇳 Tamil", callback_data="lang_ta"),
                    InlineKeyboardButton("🇮🇳 Telugu", callback_data="lang_te")
                ],
                [
                    InlineKeyboardButton("🇮🇳 Marathi",
                                         callback_data="lang_mr"),
                    InlineKeyboardButton("🇮🇳 Gujarati",
                                         callback_data="lang_gu")
                ],
                [
                    InlineKeyboardButton("🇮🇳 Kannada",
                                         callback_data="lang_kn"),
                    InlineKeyboardButton("🇮🇳 Malayalam",
                                         callback_data="lang_ml")
                ],
                [InlineKeyboardButton("🔙 Back", callback_data="start_menu")]]
    return InlineKeyboardMarkup(keyboard)


# 🔘 HELP BUTTONS
def get_help_buttons():
    keyboard = [[
        InlineKeyboardButton("📖 Basic", callback_data="basic_cmds"),
        InlineKeyboardButton("🛡 Advanced", callback_data="adv_cmds")
    ],
                [
                    InlineKeyboardButton("🧠 Experts",
                                         callback_data="expert_cmds"),
                    InlineKeyboardButton("📘 Pro Guide",
                                         callback_data="pro_cmds")
                ],
                [InlineKeyboardButton("🔙 Back", callback_data="start_menu")]]
    return InlineKeyboardMarkup(keyboard)


# 🔁 TRANSLATED WELCOME TEXT
def translate_welcome(user):
    lang = USER_LANGUAGES.get(user.id, "en")
    name = user.first_name if user else "Friend"

    if lang == "hi":
        return f"👋 <b>Hi {name}!</b>\n\n🤖 <b>MarsGroup Bot</b> आपके ग्रुप को manage करने में मदद करता है।\n\n👉🏻 Supergroup में जोड़ें और Admin बनाएं।\n\n❓ <b>Commands देखने के लिए</b> /help दबाएँ।"
    elif lang == "ur":
        return f"👋 <b>Hi {name}!</b>\n\n🤖 <b>MarsGroup Bot</b> آپ کے گروپ کو آسانی سے منظم کرتا ہے۔\n\n👉🏻 براہ کرم سپرگروپ میں شامل کریں اور ایڈمن بنائیں۔\n\n❓ /help کمانڈز دیکھنے کے لیے دبائیں۔"
    elif lang == "bn":
        return f"👋 <b>Hi {name}!</b>\n\n🤖 <b>MarsGroup Bot</b> আপনার গ্রুপ পরিচালনায় সাহায্য করে।\n\n👉🏻 সুপারগ্রুপে যোগ করুন এবং অ্যাডমিন করুন।\n\n❓ কমান্ড দেখতে /help চাপুন।"
    elif lang == "ta":
        return f"👋 <b>Hi {name}!</b>\n\n🤖 <b>MarsGroup Bot</b> உங்கள் குழுவை நிர்வகிக்க உதவுகிறது.\n\n👉🏻 சுபர்குரூப்பில் சேர்த்து அட்மின் செய்யவும்.\n\n❓ கட்டளைகளை காண /help அழுத்தவும்."
    elif lang == "te":
        return f"👋 <b>Hi {name}!</b>\n\n🤖 <b>MarsGroup Bot</b> మీ గ్రూప్‌ను నిర్వహించడంలో సహాయపడుతుంది.\n\n👉🏻 సూపర్‌గ్రూప్‌లో జోడించండి మరియు అడ్మిన్‌గా ప్రమోట్ చేయండి.\n\n❓ ఆదేశాలు చూడటానికి /help నొక్కండి."
    elif lang == "mr":
        return f"👋 <b>Hi {name}!</b>\n\n🤖 <b>MarsGroup Bot</b> तुमच्या ग्रुपचे व्यवस्थापन करण्यात मदत करतो.\n\n👉🏻 सुपरग्रुपमध्ये जोडा आणि अ‍ॅडमिन करा.\n\n❓ कमांड पाहण्यासाठी /help दाबा."
    elif lang == "gu":
        return f"👋 <b>Hi {name}!</b>\n\n🤖 <b>MarsGroup Bot</b> તમારા જૂથને મેનેજ કરવામાં મદદ કરે છે.\n\n👉🏻 મને સુપરગ્રુપમાં ઉમેરો અને એડમિન બનાવો.\n\n❓ /help દબાવો આદેશો જોવા માટે."
    elif lang == "kn":
        return f"👋 <b>Hi {name}!</b>\n\n🤖 <b>MarsGroup Bot</b> ನಿಮ್ಮ ಗುಂಪು ನಿರ್ವಹಿಸಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ.\n\n👉🏻 ನನ್ನನ್ನು ಸೂಪರ್ಗ್ರೂಪ್ನಲ್ಲಿ ಸೇರಿಸಿ ಮತ್ತು ಆಡ್ಮಿನ್ ಮಾಡಿ.\n\n❓ ಆಜ್ಞೆಗಳನ್ನಾಗೆ ನೋಡಲು /help ಒತ್ತಿ."
    elif lang == "ml":
        return f"👋 <b>Hi {name}!</b>\n\n🤖 <b>MarsGroup Bot</b> നിങ്ങളുടെ ഗ്രൂപ്പ് ലളിതമായി നിയന്ത്രിക്കാൻ സഹായിക്കുന്നു.\n\n👉🏻 എന്നെ സൂപ്പർഗ്രൂപ്പിൽ ചേർക്കുക, അഡ്മിൻ ആക്കുക.\n\n❓ /help അമർത്തി കമാൻഡുകൾ കാണുക."

    return get_welcome_message(user)


# 🛠 SAFE EDIT FUNCTION
async def safe_edit(query, new_text, new_markup):
    try:
        current_text = (query.message.text or "").strip()
        new_text = new_text.strip()
        if current_text == new_text and query.message.reply_markup == new_markup:
            return
        await query.edit_message_text(text=new_text,
                                      reply_markup=new_markup,
                                      parse_mode="HTML")
    except Exception as e:
        print(f"❌ Failed to edit message: {e}")


# 📲 CALLBACK HANDLER
async def handle_button_click(update: Update,
                              context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    if query.data == "start_menu":
        await safe_edit(query, translate_welcome(user), get_start_buttons())

    elif query.data == "language_menu":
        await safe_edit(query, "🌐 <b>Select your language:</b>",
                        get_language_buttons())

    elif query.data.startswith("lang_"):
        lang_code = query.data.split("_")[1]
        USER_LANGUAGES[user.id] = lang_code
        await safe_edit(query, translate_welcome(user), get_start_buttons())

    elif query.data == "help_menu":
        await safe_edit(query, "🧠 <b>Help Menu</b>\nChoose an option below:",
                        get_help_buttons())

    elif query.data == "basic_cmds":
        await safe_edit(
            query, "<b>📖 Basic Commands</b>\n\n"
            "👮🏻 /reload - Updates admin list\n"
            "🕵🏻 /settings - Manage group settings\n"
            "👮🏻 /ban - Ban user permanently\n"
            "👮🏻 /mute - Mute user\n"
            "👮🏻 /kick - Kick user\n"
            "👮🏻 /unban - Unban user\n"
            "👮🏻 /info - Show user info\n"
            "👮🏻 /infopvt - Info in private\n"
            "◽️ /staff - Show group staff list", get_help_buttons())

    elif query.data == "adv_cmds":
        await safe_edit(
            query, "<b>🛡 Advanced Commands</b>\n\n"
            "🔐 /lock - Lock content\n"
            "🔓 /unlock - Unlock\n"
            "📛 /purge - Bulk delete\n"
            "📍 /setwelcome - Custom welcome\n"
            "🎉 /cleanwelcome - Auto delete welcome\n"
            "🔗 /antilink - Enable anti-link", get_help_buttons())

    elif query.data == "expert_cmds":
        await safe_edit(
            query, "<b>🧠 Expert Commands</b>\n\n"
            "🧾 /log - Send logs\n"
            "📊 /stats - Bot stats\n"
            "🧹 /cleandb - Clean DB\n"
            "🔧 /maintenance - Maintenance mode\n"
            "🛠 /module - Enable/disable modules", get_help_buttons())

    elif query.data == "pro_cmds":
        await safe_edit(
            query, "<b>📘 Pro Guide</b>\n\n"
            "🚀 Full guide:\n"
            "<a href='https://github.com/ravinishayar/marsChatBot'>marsChatBot Repo</a>\n\n"
            "🧑‍💻 Contact: @ravinishayar54", get_help_buttons())

    elif query.data == "info":
        await safe_edit(
            query, "<b>ℹ️ Group Help (ChatGuard)</b>\n"
            "Developed by <a href='https://t.me/ravinishayar54'>@ravinishayar54</a>, and it is actively maintained.\n"
            "Launched in <b>2025</b> and updated regularly.\n\n"
            "<b>🤖 Bot Version:</b> 2.0\n\n"
            "<b>👤 Bot Admins:</b>\n"
            "• Created by <b>Karan</b> (👉 <a href='https://t.me/ravinishayar54'>@ravinishayar54</a>)\n"
            "• Deployment and Management by <b>Villain</b> (👉 <a href='https://t.me/iamakki001'>@iamakki001</a>)\n"
            "• Concept and Idea by the Developer\n\n"
            "⚠️ <b>This bot does not support any kind of promotion.</b>\n"
            "Its purpose is to <b>help manage your group automatically</b>.\n"
            "Just add the bot and promote it as admin — it will handle everything on its own!",
            get_start_buttons())
