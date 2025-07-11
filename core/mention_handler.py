from pyrogram.types import Message
from pyrogram import Client

# Store running mentions per chat
mention_tasks = {}


async def mention_all_pyro(client: Client, message: Message):
    chat_id = message.chat.id
    text = " ".join(message.command[1:]) or "Hey everyone 👋"

    members = []
    async for m in client.get_chat_members(chat_id):
        if not m.user.is_bot:
            members.append(m.user)

    mentions = " ".join(
        [f"[{user.first_name}](tg://user?id={user.id})" for user in members])

    # Save task so it can be cancelled
    sent = await client.send_message(chat_id,
                                     f"{text}\n\n{mentions}",
                                     disable_web_page_preview=True)
    mention_tasks[chat_id] = sent


async def mention_admins_pyro(client: Client, message: Message):
    chat_id = message.chat.id
    text = " ".join(message.command[1:]) or "Calling all admins 🔥"

    admins = []
    async for m in client.get_chat_members(chat_id, filter="administrators"):
        if not m.user.is_bot:
            admins.append(m.user)

    if not admins:
        await message.reply("No admins found in this group.")
        return

    mentions = " ".join(
        [f"[{user.first_name}](tg://user?id={user.id})" for user in admins])

    sent = await client.send_message(chat_id,
                                     f"{text}\n\n{mentions}",
                                     disable_web_page_preview=True)
    mention_tasks[chat_id] = sent


async def cancel_mention_pyro(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in mention_tasks:
        try:
            await client.delete_messages(chat_id, mention_tasks[chat_id].id)
            await message.reply("✅ Mention cancelled.")
            del mention_tasks[chat_id]
        except Exception as e:
            await message.reply(f"⚠️ Could not cancel mention: {e}")
    else:
        await message.reply("❌ No active mention to cancel.")
