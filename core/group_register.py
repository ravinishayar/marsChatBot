REGISTERED_GROUPS = set()


def register_group(chat_id: int):
    REGISTERED_GROUPS.add(chat_id)
    print(f"[+] Group registered: {chat_id}")
