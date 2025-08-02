# cogs/xp_cog.py
import discord
from discord.ext import commands
import json
import os
import time
from datetime import datetime, timezone

DATA_PATH = "data/user_data.json"
COOLDOWN_SECONDS = 180

def load_data():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}

def save_data(data):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

class XPCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def ensure_user(self, data, user_id):
        """Khởi tạo cấu trúc dữ liệu cho user nếu chưa có."""
        if user_id not in data:
            data[user_id] = {
                "xp": 0,
                "level": 1,
                "daily_messages": 0,
                "daily_bonus_claimed": False,
                "last_message_ts": 0,
                "last_reset_date": None  # format "YYYY-MM-DD"
            }

    def reset_daily_if_needed(self, user):
        """Reset daily_messages & daily_bonus_claimed vào lúc 00:00 UTC."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        if user.get("last_reset_date") != today:
            user["daily_messages"] = 0
            user["daily_bonus_claimed"] = False
            user["last_reset_date"] = today

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not isinstance(message.channel, discord.TextChannel):
            return

        user_id = str(message.author.id)
        data = load_data()
        self.ensure_user(data, user_id)
        user = data[user_id]

        # Reset daily counter nếu đã qua 00:00 UTC
        self.reset_daily_if_needed(user)

        now_ts = time.time()
        # Kiểm tra cooldown 60s
        if now_ts - user.get("last_message_ts", 0) < COOLDOWN_SECONDS:
            return

        # Cập nhật thời gian lần nhắn cuối
        user["last_message_ts"] = now_ts

        # +1 XP cho tin nhắn
        user["xp"] += 1
        # Tăng bộ đếm tin nhắn hàng ngày
        user["daily_messages"] += 1

        # Nếu đạt đủ 10 tin và chưa nhận bonus hôm nay
        if user["daily_messages"] >= 10 and not user["daily_bonus_claimed"]:
            user["xp"] += 25
            user["daily_bonus_claimed"] = True
            try:
                await message.channel.send(
                    f"🎁 {message.author.mention} đã hoàn thành 10 tin nhắn hôm nay, nhận thêm **25 XP**!",
                    delete_after=10
                )
            except:
                pass

        save_data(data)
        # Cho phép các cog khác xử lý lệnh
        await self.bot.process_commands(message)

@commands.command(name="rank")
    async def rank(self, ctx):
        from utils.xp_utils import get_level, get_xp_for_next_level, get_role_for_level, get_rank
        from utils.data_manager import read_json
        
        user = ctx.author
        user_id = str(user.id)

        user_data = read_json("data/user_data.json")
        if user_id not in user_data:
            return await ctx.send("❌ Bạn chưa có dữ liệu XP nào.")

        xp = user_data[user_id].get("xp", 0)
        level = get_level(xp)
        xp_needed = get_xp_for_next_level(level)
        role_info = get_role_for_level(level)
        rank_position, total_players = get_rank(user_id)

        embed = discord.Embed(
            title=f"📊 Rank của {user.display_name}:",
            description=(
                f"Cấp độ: {level} | XP: {xp} / {xp_needed}\n"
                f"Vai trò hiện tại: {role_info['icon']} {role_info['name']}\n"
                f"Xếp hạng: #{rank_position}/{total_players}"
            ),
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(XPCog(bot))