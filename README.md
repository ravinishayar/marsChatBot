# 🤖 MarsGroupManager Bot

**MarsGroupManager** is a multipurpose Telegram group management bot with powerful Hindi auto-replies, emoji responses, link protection, and warning system. Perfect for desi groups that need control and chat interaction in one bot.

---

## 🚀 Features

- 🤖 **Hindi Auto Replies** – Replies naturally to common Hindi chat phrases.
- 😊 **Emoji Reactions** – Replies to emoji-only messages.
- 🚫 **Link Deletion** – Automatically deletes any message containing a link (even from bots).
- ⚠️ **Warning System** – Use `/warn` command; 2 warnings = auto-ban.
- 🙋‍♂️ **Welcome Message** – Sends custom welcome messages with image and buttons.
- 🤖 **Bot Join Greet** – Greets the group when the bot is added.

---

## 📦 Installation

### 1. Clone the Bot

```bash
git clone https://github.com/ravinishayar/marsChatBot.git
cd marsChatBot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

Make sure you add the following secrets:

| Variable         | Description                                 |
|------------------|---------------------------------------------|
| `BOT_TOKEN`       | From @BotFather                             |
| `LOGGER_GROUP_ID`| Group ID where logs will be sent (start with `-100`) |

### 4. Run the Bot

```bash
python main.py
```

---

## 📁 Project Structure

```
marsChatBot/
├── core/
│   ├── __init__.py                # Central import
│   ├── start_handler.py           # /start command logic
│   ├── group_join_handler.py      # Greets when bot or user joins
│   ├── warnsystem.py              # /warn and auto-ban logic
│   ├── responses.py               # Handles chat replies
│   ├── link_protection.py         # Link delete system
│   └── inline_buttons.py          # Button layout
│
├── main.py                        # Bot setup and handler registration
├── requirements.txt               # All required Python packages
├── welcome_message.txt            # Saved welcome message text
├── warns.json                     # Stores warning counts
├── README.md                      # You're here :)
```

---

## ✨ Usage

- `/start` — Shows bot info with image and buttons
- `/setwelcome` — Sets a new welcome message
- `/warn` — Warns a user (must be used in reply)
- ✨ Chat normally — bot replies if your message matches

---

## 🧑 Author

Made with ❤️ by [@ravinishayar](https://t.me/ravinishayar54)

---

## 📜 License

MIT – Free to use, modify, share.


---

## 🚀 Deploy the Bot

You can deploy this bot instantly:

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/ravinishayar/marsChatBot)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/YOUR_RAILWAY_TEMPLATE_ID)

> 🔧 Replace `YOUR_RAILWAY_TEMPLATE_ID` with your actual template ID if available.

---

## 🧑‍💻 Maintainer

- 👤 **Created by**: [@ravinishayar](https://github.com/ravinishayar)
- 💬 Telegram: [t.me/ravinishayar](https://t.me/ravinishayar54)

---

## ⭐ Support

If you like this bot, consider starring 🌟 the repository and sharing it with friends. Contributions and feedback are welcome!

