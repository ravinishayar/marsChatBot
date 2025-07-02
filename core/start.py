# core/start.py


# 🔁 Reusable welcome message generator
def get_welcome_message(user):
    name = user.first_name if user else "Friend"
    return (
        f"👋 <b>Hi {name}!</b>\n\n"
        "🤖 <b>Group Help</b> is the most complete Bot to help you manage your groups easily and safely!\n\n"
        "👉🏻 <b>Add me in a Supergroup</b> and promote me as Admin to let me get in action!\n\n"
        "❓ <b>WHICH ARE THE COMMANDS?</b>\n"
        "Press <code>/help</code> to see all the commands and how they work!")
