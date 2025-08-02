import json
import os

DATA_PATH = "data/user_data.json"

def load_data():
    if not os.path.exists(DATA_PATH):
        return {}
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def ensure_user_exists(user_id):
    data = load_data()
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {
            "xp": 0,
            "level": 1,
            "daily_messages": 0,
            "last_xp_time": None
        }
        save_data(data)
    return data

def add_xp(user_id, xp_amount):
    data = ensure_user_exists(user_id)
    user_data = data[str(user_id)]

    old_level = user_data["level"]
    user_data["xp"] += xp_amount

    # Calculate level using standardized formula
    new_level = 1
    total_xp = user_data["xp"]
    while total_xp >= (50 + new_level * 25):
        total_xp -= (50 + new_level * 25)
        new_level += 1

    user_data["level"] = new_level
    save_data(data)

    return old_level, new_level

def add_daily_message(user_id):
    data = ensure_user_exists(user_id)
    user_data = data[str(user_id)]
    user_data["daily_messages"] = user_data.get("daily_messages", 0) + 1
    save_data(data)

def reset_all_user_daily_data():
    data = load_data()
    for user_id in data:
        data[user_id]["daily_messages"] = 0
    save_data(data)
    print(f"[XP MANAGER] Reset daily data for {len(data)} users")