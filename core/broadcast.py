import json
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from core.broadcast_utils import load_users, load_groups

# 🔥 Your Logger Group ID (replace with your group ID)
LOGGER_GROUP_ID = -1002533639590  # 👈 Replace this with your logger group ID


# ✅ Broadcast to all users
async def user_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        message_to_send = update.message.reply_to_message.text
    elif context.args:
        message_to_send = " ".join(context.args)
    else:
        await update.message.reply_text(
            "⚠️ Usage: /broadcast <your message> or reply to a message.")
        return

    users = load_users()
    success = 0
    failed = 0

    for user_id in users.copy():
        try:
            await context.bot.send_message(chat_id=user_id,
                                           text=message_to_send)
            success += 1
        except Exception as e:
            print(f"❌ Failed to send to {user_id}: {e}")
            failed += 1
            users.remove(user_id)
            with open("broadcast_users.json", "w") as f:
                json.dump(users, f, indent=2)

    await update.message.reply_text(
        f"✅ User Broadcast completed.\n📬 Delivered: {success}\n❌ Failed: {failed}"
    )


# ✅ Broadcast to all groups
async def group_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        message_to_send = update.message.reply_to_message.text
    elif context.args:
        message_to_send = " ".join(context.args)
    else:
        await update.message.reply_text(
            "⚠️ Usage: /groupbroadcast <your message> or reply to a message.")
        return

    groups = load_groups()
    success = 0
    failed = 0
    failed_groups_info = []

    for group_id in groups.copy():
        try:
            await context.bot.send_message(chat_id=group_id,
                                           text=message_to_send)
            success += 1
        except Exception as e:
            print(f"❌ Failed to send to {group_id}: {e}")
            failed += 1
            # 🗑 Remove inactive group
            groups.remove(group_id)
            with open("broadcast_groups.json", "w") as f:
                json.dump(groups, f, indent=2)

            try:
                # 👇 Try to fetch group info
                chat = await context.bot.get_chat(group_id)
                group_name = chat.title or "No Title"
                group_username = f"@{chat.username}" if chat.username else "No Username"
            except Exception as fetch_error:
                group_name = "Unknown"
                group_username = "Unknown"

            failed_groups_info.append(
                f"📛 {group_name}\n🆔 {group_id}\n🔗 {group_username}")

    await update.message.reply_text(
        f"✅ Group Broadcast completed.\n📬 Delivered: {success}\n❌ Failed: {failed}"
    )

    # ✅ Send failed group list to logger group
    if failed_groups_info:
        failed_message = "⚠️ *Failed to send broadcast to these groups:*\n\n" + "\n\n".join(
            failed_groups_info)
        try:
            await context.bot.send_message(chat_id=LOGGER_GROUP_ID,
                                           text=failed_message,
                                           parse_mode="Markdown",
                                           disable_web_page_preview=True)
        except Exception as logger_error:
            print(
                f"❌ Failed to send failed groups info to logger: {logger_error}"
            )


# ✅ Return Handlers for main.py
def get_broadcast_handlers():
    return [
        CommandHandler("broadcast", user_broadcast),
        CommandHandler("groupbroadcast", group_broadcast),
    ]
