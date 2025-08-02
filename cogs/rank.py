
import discord
from discord.ext import commands
import json
import os

class Rank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_path = "data/user_data.json"

    def get_user_level_data(self, user_id):
        if not os.path.exists(self.data_path):
            return {"xp": 0, "level": 1}
        with open(self.data_path, "r") as f:
            data = json.load(f)
        user_id = str(user_id)
        if user_id not in data:
            return {"xp": 0, "level": 1}
        return data[user_id]

    def get_user_rank(self, user_id):
        if not os.path.exists(self.data_path):
            return None, 0
        with open(self.data_path, "r") as f:
            data = json.load(f)
        sorted_users = sorted(data.items(), key=lambda x: (x[1].get("level", 1), x[1].get("xp", 0)), reverse=True)
        for index, (uid, info) in enumerate(sorted_users):
            if uid == str(user_id):
                return index + 1, len(sorted_users)
        return None, len(sorted_users)

    def get_role_name_by_level(self, level):
        level_roles = {
            1: "🧍‍♂️ Dân thường",
            5: "🌱 Tổ trưởng khu phố",
            10: "🧑‍💼 Cán bộ xã",
            15: "🎯 Chủ nhiệm CLB",
            20: "🏛️ Quận trưởng",
            25: "💰 Trưởng phòng tài chính",
            30: "🏙️ Phó chủ tịch TP",
            35: "🎉 Bộ trưởng sự kiện",
            40: "⚔️ Đặc vụ XP",
            45: "🕵️‍♂️ Thanh tra cấp cao",
            50: "👑 Lãnh đạo tối cao",
        }
        role = "Chưa có vai trò"
        for lv in sorted(level_roles.keys(), reverse=True):
            if level >= lv:
                role = level_roles[lv]
                break
        return role

    def get_xp_needed_for_next_level(self, level):
        return 50 + level * 25

    @commands.command(name="rank")
    async def rank(self, ctx):
        user = ctx.author
        data = self.get_user_level_data(user.id)
        level = data.get("level", 1)
        xp = data.get("xp", 0)
        xp_needed = self.get_xp_needed_for_next_level(level)
        role_name = self.get_role_name_by_level(level)
        rank_pos, total_users = self.get_user_rank(user.id)

        embed = discord.Embed(
            title=f"📊 Rank của {user.display_name}:",
            description=(
                f"Cấp độ: `{level}` | XP: `{xp} / {xp_needed}`\n"
                f"Vai trò hiện tại: **{role_name}**\n"
                f"Xếp hạng: `#{rank_pos}/{total_users}`" if rank_pos else f"Xếp hạng: `Chưa có/{total_users}`"
            ),
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Rank(bot))
