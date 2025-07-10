from pyrogram import Client
import os

# 🔑 Load API details from ENV
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")

# ✅ Create Pyrogram client
pyro_client = Client(
    name="bot_session",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
)
