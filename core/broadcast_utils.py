# core/broadcast_utils.py
import json
import os

# File paths
USER_FILE = "broadcast_users.json"
GROUP_FILE = "broadcast_groups.json"


# ✅ Load all user IDs
def load_users():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump([], f)
    with open(USER_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


# ✅ Save user if not already saved
def save_user_if_not_exists(user_id: int):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(USER_FILE, "w") as f:
            json.dump(users, f, indent=2)


# ✅ Load all group IDs
def load_groups():
    if not os.path.exists(GROUP_FILE):
        with open(GROUP_FILE, "w") as f:
            json.dump([], f)
    with open(GROUP_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


# ✅ Save group if not already saved
def save_group_if_not_exists(group_id: int):
    groups = load_groups()
    if group_id not in groups:
        groups.append(group_id)
        with open(GROUP_FILE, "w") as f:
            json.dump(groups, f, indent=2)
