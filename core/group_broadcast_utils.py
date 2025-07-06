import json
import os

GROUP_LOG = "broadcast_groups.json"


def load_groups():
    if not os.path.exists(GROUP_LOG):
        with open(GROUP_LOG, "w") as f:
            json.dump({"groups": []}, f, indent=2)
        return []

    try:
        with open(GROUP_LOG, "r") as f:
            data = json.load(f)
            return data.get("groups", [])
    except json.JSONDecodeError:
        return []


def save_group(chat_id: int, chat_title: str):
    groups = load_groups()
    for group in groups:
        if group["id"] == chat_id:
            return  # already saved

    groups.append({"id": chat_id, "title": chat_title})
    with open(GROUP_LOG, "w") as f:
        json.dump({"groups": groups}, f, indent=2)
