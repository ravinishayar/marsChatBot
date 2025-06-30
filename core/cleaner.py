from datetime import datetime, timedelta
from telegram.constants import ChatMemberStatus
from telegram import Message
from telegram.error import TelegramError

REGISTERED_GROUPS = set()
MEDIA_MESSAGES = {}


# Group registration
def register_group(chat_id: int):
    if chat_id not in REGISTERED_GROUPS:
        REGISTERED_GROUPS.add(chat_id)
        MEDIA_MESSAGES[chat_id] = []
        print(f"[+] Group registered for cleaner: {chat_id}")


# Store incoming media messages
def store_media_message(message: Message):
    chat_id = message.chat_id
    if chat_id not in MEDIA_MESSAGES:
        MEDIA_MESSAGES[chat_id] = []
    MEDIA_MESSAGES[chat_id].append((message.message_id, message.date))


# Task to auto-delete media
async def auto_delete_media_task(bot):
    print(
        f"[🧹] Running auto-clean task... Total groups: {len(REGISTERED_GROUPS)}"
    )

    for chat_id in list(REGISTERED_GROUPS):
        deleted_in_group = 0
        try:
            # Check bot is admin
            member = await bot.get_chat_member(chat_id, bot.id)
            if member.status not in [
                    ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER
            ]:
                continue

            messages = MEDIA_MESSAGES.get(chat_id, [])
            new_messages = []

            for message_id, msg_date in messages:
                # Convert to naive datetime
                msg_date_naive = msg_date.replace(tzinfo=None)

                if datetime.utcnow() - msg_date_naive > timedelta(minutes=2):
                    try:
                        await bot.delete_message(chat_id, message_id)
                        print(
                            f"[🗑️] Deleted message {message_id} in {chat_id}")
                        deleted_in_group += 1
                    except TelegramError:
                        pass
                else:
                    new_messages.append((message_id, msg_date))

            MEDIA_MESSAGES[chat_id] = new_messages

            # ✅ Send notification if something was deleted
            if deleted_in_group > 0:
                try:
                    await bot.send_message(
                        chat_id,
                        f"🧹 Deleted {deleted_in_group} old media message(s)")
                except TelegramError as e:
                    print(f"[!] Failed to send notification in {chat_id}: {e}")

        except Exception as e:
            print(f"[!] Error in cleaner for group {chat_id}: {e}")
