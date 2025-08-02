
import json
import os

DATA_PATH = "data/user_data.json"

def load_data():
    """Load user data from JSON file"""
    if not os.path.exists(DATA_PATH):
        return {}
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    """Save user data to JSON file"""
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_user_data(user_id):
    """Get data for a specific user"""
    data = load_data()
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {
            "xp": 0,
            "level": 1,
            "daily_messages": 0,
            "daily_bonus_claimed": False,
            "last_message_ts": 0,
            "last_reset_date": None
        }
        save_data(data)
    return data[user_id]

def update_user_data(user_id, user_data):
    """Update data for a specific user"""
    data = load_data()
    data[str(user_id)] = user_data
    save_data(data)
