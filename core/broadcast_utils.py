import json
import os

BROADCAST_LOG = "broadcast_users.json"


# Load users or groups from file
def load_users():
    if not os.path.exists(BROADCAST_LOG):
        with open(BROADCAST_LOG, "w") as f:
            json.dump([], f)
        return []

    try:
        with open(BROADCAST_LOG, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


# Save a new user or group ID if not already present
def save_user(chat_id: int):
    users = load_users()

    if chat_id not in users:
        users.append(chat_id)
        with open(BROADCAST_LOG, "w") as f:
            json.dump(users, f, indent=2)
