from telegram import Update
from telegram.ext import ContextTypes
from core.database import get_user_collection  # ✅ Import collection function

# ✅ Get collection
users = get_user_collection()


# ✅ User tracking handler with name history
async def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user = update.effective_user
    if not user:
        return

    existing_user = users.find_one({"_id": user.id})
    current_name = user.first_name

    if existing_user:
        # पुराना नाम history से निकालना
        name_history = existing_user.get("name_history", [])
        if current_name not in name_history:
            name_history.append(current_name)

        users.update_one(
            {"_id": user.id},
            {
                "$set": {
                    "username": user.username,
                    "first_name": current_name,
                    "last_name": user.last_name,
                    "name_history": name_history
                }
            },
        )
    else:
        # नया यूज़र, नई history शुरू करो
        users.insert_one({
            "_id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "name_history": [user.first_name]
        })
