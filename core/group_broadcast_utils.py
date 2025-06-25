# core/group_broadcast_utils.py
import json
import os

GROUP_LOG = "broadcast_groups.json"


def load_groups():
    if not os.path.exists(GROUP_LOG):
        with open(GROUP_LOG, "w") as f:
            json.dump([], f)
        return []

    try:
        with open(GROUP_LOG, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_group(chat_id: int):
    groups = load_groups()
    if chat_id not in groups:
        groups.append(chat_id)
        with open(GROUP_LOG, "w") as f:
            json.dump(groups, f, indent=2)
