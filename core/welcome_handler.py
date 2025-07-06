import os
from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from core.cleaner import register_group  # ✅ import register_group

# ✅ Custom Background Image URL
WELCOME_IMAGE_URL = "https://i.ibb.co/93sbLjyt/20250704-160350.jpg"


async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome image with custom background and user DP."""
    # ✅ Register group to ensure it's tracked
    register_group(update.effective_chat.id)

    # ✅ Check if bot is admin in group
    bot_member = await context.bot.get_chat_member(update.effective_chat.id,
                                                   context.bot.id)
    if bot_member.status not in ["administrator", "creator"]:
        return  # Bot is not admin, skip

    new_member = update.message.new_chat_members[0]
    group_name = update.effective_chat.title
    username = f"@{new_member.username}" if new_member.username else new_member.full_name

    # ✅ Get Group Owner Info Dynamically
    try:
        admins = await context.bot.get_chat_administrators(
            update.effective_chat.id)
        owner = next((a.user for a in admins if a.status == "creator"), None)
        if owner:
            owner_username = f"@{owner.username}" if owner.username else owner.full_name
        else:
            owner_username = "Group Owner"
    except Exception:
        owner_username = "Group Owner"

    # ✅ Download background image from URL
    response = requests.get(WELCOME_IMAGE_URL)
    background = Image.open(BytesIO(response.content)).convert("RGBA")

    # ✅ Try to get user profile photo
    photos = await context.bot.get_user_profile_photos(new_member.id, limit=1)
    if photos.total_count > 0:
        file_id = photos.photos[0][-1].file_id
        file = await context.bot.get_file(file_id)
        photo_bytes = await file.download_as_bytearray()
        user_dp = Image.open(BytesIO(photo_bytes)).resize(
            (300, 300)).convert("RGBA")
    else:
        # No DP → Create placeholder circle
        user_dp = Image.new("RGBA", (300, 300), (200, 200, 200, 255))
        draw_dp = ImageDraw.Draw(user_dp)
        draw_dp.text((100, 130), "No DP", fill="black")

    # ✅ Paste user DP in circle
    mask = Image.new("L", user_dp.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0) + user_dp.size, fill=255)
    dp_position = (
        (background.width - user_dp.width) // 2, 150)  # Center horizontally
    background.paste(user_dp, dp_position, mask)

    # ✅ Add Text Overlay (Only Welcome Title, Username & Group Name)
    draw = ImageDraw.Draw(background)
    try:
        font_big = ImageFont.truetype("arial.ttf", 60)
        font_small = ImageFont.truetype("arial.ttf", 40)
    except:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # 🎉 Welcome Text
    draw.text((50, 20), "🎉✨ WELCOME ✨🎉", font=font_big, fill="yellow")
    # User and Group Name
    draw.text((50, 500), f"Hey {username}", font=font_small, fill="white")
    draw.text((50, 550), f"🌟 {group_name} 🌟", font=font_small, fill="white")

    # ✅ Save Output Image
    output = BytesIO()
    output.name = "welcome.png"
    background.save(output, format="PNG")
    output.seek(0)

    # ✅ Stylish Caption with Rules Box
    caption = ("🎉✨ 𝑾𝑬𝑳𝑪𝑶𝑴𝑬 ✨🎉\n\n"
               f"🙋‍♂️ 𝐇𝐞𝐲 {username},\n\n"
               f"🌟 𝑾𝒆 𝒂𝒓𝒆 𝒔𝒐 𝒈𝒍𝒂𝒅 𝒕𝒐 𝒉𝒂𝒗𝒆 𝒚𝒐𝒖 𝒊𝒏 🌟\n"
               f"💎 {group_name} 💎\n\n"
               "╭──────📜 *RULES* 📜──────╮\n"
               "1️⃣ *Be Respectful* 😇\n"
               "2️⃣ *No Spamming* 🚫\n"
               "3️⃣ *No Hate Speech* ❌\n"
               "4️⃣ *Use English/Hindi Only* 📚\n"
               "5️⃣ *Admin's words are final* 👮‍♂️\n"
               "╰────────────────────────╯\n\n"
               f"📞 *Contact Owner:* {owner_username}")

    # ✅ Send welcome photo with fancy rules caption
    await update.effective_chat.send_photo(photo=InputFile(output),
                                           caption=caption,
                                           parse_mode="Markdown")
