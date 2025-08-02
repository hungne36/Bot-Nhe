
import discord
from discord.ext import commands
from discord import app_commands
from utils.data_manager import read_json, write_json
from datetime import datetime
import random

def get_random_reward(level):
    """Generate random reward based on user level"""
    rewards = []
    
    # Currency rewards
    base_amount = 100 + (level * 50)
    rewards.extend([
        {"name": f"{base_amount} xu", "amount": base_amount, "type": "currency"},
        {"name": f"{base_amount * 2} xu", "amount": base_amount * 2, "type": "currency"},
        {"name": f"{base_amount // 2} xu", "amount": base_amount // 2, "type": "currency"}
    ])
    
    # Level-based special rewards
    if level >= 10:
        rewards.append({"name": "Bonus XP", "amount": 100, "type": "xp"})
    if level >= 20:
        rewards.append({"name": "Premium Item", "amount": 1, "type": "item"})
    
    return random.choice(rewards)

class Mission(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mission", description="Nhận phần thưởng nếu bạn đủ 30 XP/ngày!")
    async def mission(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        now = datetime.utcnow()
        today_str = now.strftime("%Y-%m-%d")

        data = read_json("data/user_data.json")
        user = data.get(user_id)

        if not user:
            await interaction.response.send_message("❌ Bạn chưa có dữ liệu người dùng.", ephemeral=True)
            return

        # Kiểm tra đã nhận hôm nay chưa
        if user.get("lastMission") == today_str:
            await interaction.response.send_message("❌ Bạn đã nhận phần thưởng nhiệm vụ hôm nay rồi.", ephemeral=True)
            return

        # Kiểm tra đủ điều kiện (daily messages >= 10)
        if user.get("daily_messages", 0) < 10:
            await interaction.response.send_message("❌ Bạn cần gửi ít nhất 10 tin nhắn hôm nay để nhận phần thưởng!", ephemeral=True)
            return

        # Random phần thưởng
        level = user.get("level", 1)
        reward = get_random_reward(level)

        # Cập nhật dữ liệu theo phần thưởng
        if reward["type"] == "currency":
            user["balance"] = user.get("balance", 0) + reward["amount"]
        elif reward["type"] == "xp":
            user["xp"] = user.get("xp", 0) + reward["amount"]
        elif reward["type"] == "item":
            if "items" not in user:
                user["items"] = []
            user["items"].append(reward["name"])

        user["lastMission"] = today_str
        write_json("data/user_data.json", data)

        embed = discord.Embed(
            title="🎁 Nhiệm vụ hoàn thành!",
            description=f"Bạn đã nhận: **{reward['name']}**",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Mission(bot))
