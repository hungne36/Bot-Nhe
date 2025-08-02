import discord
from discord.ext import commands
from discord import app_commands
import json
import random
from datetime import datetime, timedelta, timezone
import os

# Đường dẫn file dữ liệu người dùng
DATA_PATH = "data/user_data.json"

# Load dữ liệu từ file
def load_data():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Lưu dữ liệu vào file
def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Tạo danh sách phần thưởng hiếm
def get_random_reward(level):
    rewards = [
        {"name": "Pet Ticket 🎟️", "type": "item"},
        {"name": "Loot Box 🎁", "type": "item"},
        {"name": "XP Booster ⚡", "type": "item"},
        {"name": "Pet Attractor 🧲", "type": "item"},
        {"name": "500 Xu 💰", "type": "currency", "amount": 500},
        {"name": "Rename Token 📝", "type": "item"}
    ]
    if level < 40:
        rewards.append({"name": "1 Level Up ⬆️", "type": "level"})

    return random.choice(rewards)

class Mission(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mission", description="Nhận vật phẩm hiếm nếu bạn đủ 30 XP/ngày!")
    async def mission(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        now = datetime.utcnow()
        today_str = now.strftime("%Y-%m-%d")

        data = load_data()
        user = data.get(user_id)

        if not user:
            await interaction.response.send_message("Bạn chưa có dữ liệu người dùng.", ephemeral=True)
            return

        # Kiểm tra đã nhận hôm nay chưa
        if user.get("lastMission") == today_str:
            await interaction.response.send_message("Bạn đã nhận phần thưởng nhiệm vụ hôm nay rồi.", ephemeral=True)
            return

        # Kiểm tra đủ XP chưa
        if user.get("dailyXP", 0) < 30:
            await interaction.response.send_message("Bạn cần cày ít nhất 30 XP hôm nay để nhận phần thưởng!", ephemeral=True)
            return

        # Random phần thưởng
        level = user.get("level", 1)
        reward = get_random_reward(level)

        # Cập nhật dữ liệu theo phần thưởng
        if reward["type"] == "currency":
            user["balance"] = user.get("balance", 0) + reward["amount"]
        elif reward["type"] == "level":
            user["level"] += 1
            user["xp"] += 100  # Cho thêm XP tương ứng
        else:
            user.setdefault("items", []).append(reward["name"])

        user["lastMission"] = today_str
        save_data(data)

        await interaction.response.send_message(
            f"🎉 Bạn đã nhận được **{reward['name']}** từ nhiệm vụ hôm nay!", ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Mission(bot))