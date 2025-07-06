from telegram import Update, InputFile
from telegram.ext import ContextTypes
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests

# ✅ Custom Background Image URL
WELCOME_IMAGE_URL = "https://i.ibb.co/93sbLjyt/20250704-160350.jpg"


# ✅ Step 1: Admin sets the welcome system
async def set_welcome_start(update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
    # Save enable flag for group
    context.chat_data["welcome_enabled"] = True
    await update.message.reply_text(
        "✅ इस ग्रुप में stylish welcome system enable हो गया!\n"
        "अब से नए मेंबर्स के लिए fancy welcome भेजा जाएगा।")


# ✅ Step 2: Send fancy welcome image to new members
async def welcome_new_member(update: Update,
                             context: ContextTypes.DEFAULT_TYPE):
    # Check if welcome system is enabled for this chat
    if not context.chat_data.get("welcome_enabled"):
        return

    bot_id = context.bot.id
    for member in update.message.new_chat_members:
        if member.id == bot_id:
            continue  # ⛔ Don't welcome the bot itself

        username = f"@{member.username}" if member.username else member.full_name
        group_name = update.effective_chat.title

        # ✅ Get Group Owner Info
        try:
            admins = await context.bot.get_chat_administrators(
                update.effective_chat.id)
            owner = next((a.user for a in admins if a.status == "creator"),
                         None)
            if owner:
                owner_username = f"@{owner.username}" if owner.username else owner.full_name
            else:
                owner_username = "Group Owner"
        except Exception:
            owner_username = "Group Owner"

        # ✅ Download background image
        response = requests.get(WELCOME_IMAGE_URL)
        background = Image.open(BytesIO(response.content)).convert("RGBA")

        # ✅ Try to get user profile photo
        photos = await context.bot.get_user_profile_photos(member.id, limit=1)
        if photos.total_count > 0:
            file_id = photos.photos[0][-1].file_id
            file = await context.bot.get_file(file_id)
            photo_bytes = await file.download_as_bytearray()
            user_dp = Image.open(BytesIO(photo_bytes)).resize(
                (300, 300)).convert("RGBA")
        else:
            # No DP → Placeholder circle
            user_dp = Image.new("RGBA", (300, 300), (200, 200, 200, 255))
            draw_dp = ImageDraw.Draw(user_dp)
            draw_dp.text((100, 130), "No DP", fill="black")

        # ✅ Paste user DP in circle
        mask = Image.new("L", user_dp.size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0) + user_dp.size, fill=255)
        dp_position = ((background.width - user_dp.width) // 2, 150)
        background.paste(user_dp, dp_position, mask)

        # ✅ Add Welcome Text
        draw = ImageDraw.Draw(background)
        try:
            font_big = ImageFont.truetype("arial.ttf", 60)
            font_small = ImageFont.truetype("arial.ttf", 40)
        except:
            font_big = ImageFont.load_default()
            font_small = ImageFont.load_default()

        draw.text((50, 20), "🎉✨ WELCOME ✨🎉", font=font_big, fill="yellow")
        draw.text((50, 500), f"Hey {username}", font=font_small, fill="white")
        draw.text((50, 550),
                  f"🌟 {group_name} 🌟",
                  font=font_small,
                  fill="white")

        # ✅ Save Output Image
        output = BytesIO()
        output.name = "welcome.png"
        background.save(output, format="PNG")
        output.seek(0)

        # ✅ Stylish Caption
        caption = ("🎉✨ 𝑾𝑬𝑳𝑪𝑶𝑴𝑬 ✨🎉\n\n"
                   f"🙋‍♂️ 𝐇𝐞𝐲 {username},\n\n"
                   f"🌟 𝑾𝒆 𝒂𝒓𝒆 𝒈𝒍𝒂𝒅 𝒕𝒐 𝒉𝒂𝒗𝒆 𝒚𝒐𝒖 𝒊𝒏 🌟\n"
                   f"💎 {group_name} 💎\n\n"
                   "╭──────📜 *RULES* 📜──────╮\n"
                   "1️⃣ *Be Respectful* 😇\n"
                   "2️⃣ *No Spamming* 🚫\n"
                   "3️⃣ *No Hate Speech* ❌\n"
                   "4️⃣ *Use English/Hindi Only* 📚\n"
                   "5️⃣ *Admin's words are final* 👮‍♂️\n"
                   "╰────────────────────────╯\n\n"
                   f"📞 *Contact Owner:* {owner_username}")

        await update.effective_chat.send_photo(photo=InputFile(output),
                                               caption=caption,
                                               parse_mode="Markdown")
