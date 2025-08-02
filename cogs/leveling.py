import discord
from discord.ext import commands
import json
import asyncio

DATA_PATH = "data/user_data.json"

ROLES_BY_LEVEL = {
    1: "🧍‍♂️ Dân thường",
    5: "🌱 Tổ trưởng dân phố",
    10: "🧑‍💼 Cán bộ xã",
    15: "🎯 Chủ nhiệm CLB",
    20: "🏛️ Quận trưởng",
    25: "💰 Trưởng phòng tài chính",
    30: "🏙️ Phó chủ tịch TP",
    35: "🎉 Bộ trưởng sự kiện",
    40: "⚔️ Đặc vụ XP",
    45: "🕵️‍♂️ Thanh tra cấp cao",
    50: "👑 Lãnh đạo tối cao"
}

def load_data():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_level_role(level):
    levels = sorted(ROLES_BY_LEVEL.keys())
    role_name = ROLES_BY_LEVEL[1]
    for lv in levels:
        if level >= lv:
            role_name = ROLES_BY_LEVEL[lv]
    return role_name

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def update_roles(self, member, new_level):
        guild = member.guild
        if not guild:
            return

        role_name = get_level_role(new_level)
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            print(f"[WARN] Role '{role_name}' chưa tồn tại trên server.")
            return

        # Gỡ các role cấp thấp hơn (nếu có)
        roles_to_remove = []
        for lv, rname in ROLES_BY_LEVEL.items():
            r = discord.utils.get(guild.roles, name=rname)
            if r in member.roles and r.name != role_name:
                roles_to_remove.append(r)

        if roles_to_remove:
            await member.remove_roles(*roles_to_remove)

        if role not in member.roles:
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not isinstance(message.channel, discord.TextChannel):
            return

        user_id = str(message.author.id)
        data = load_data()

        # Create new user data and assign initial role
        if user_id not in data:
            data[user_id] = {
                "xp": 0,
                "level": 1,
                "balance": 0,
                "dailyXP": 0,
                "lastMission": "",
                "messages": 0,
                "items": [],
                "lastMessage": None,
                "lastDaily": None,
                "lastDailyXP": None,
                "xpBoostExpire": None
            }
            save_data(data)

            # ✅ Assign level 1 role for new users
            await self.update_roles(message.author, 1)

        user = data[user_id]

        # Cộng XP và dailyXP
        user["xp"] += 1
        user["dailyXP"] = user.get("dailyXP", 0) + 1
        user["messages"] = user.get("messages", 0) + 1

        # Mỗi 10 tin nhắn → cộng thêm 25 XP và reset đếm
        if user["messages"] >= 10:
            user["xp"] += 25
            user["messages"] = 0

        # Tính XP cần cho level tiếp theo
        current_level = user["level"]
        xp_needed = current_level * 100

        leveled_up = False
        # Lên cấp
        while user["xp"] >= xp_needed:
            user["xp"] -= xp_needed
            user["level"] += 1
            current_level = user["level"]
            xp_needed = current_level * 100
            leveled_up = True

        save_data(data)

        if leveled_up:
            await self.update_roles(message.author, user["level"])
            try:
                await message.channel.send(f"🎉 {message.author.mention} đã lên **Level {user['level']}** và nhận role **{get_level_role(user['level'])}**!", delete_after=5)
            except:
                pass

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(Leveling(bot))