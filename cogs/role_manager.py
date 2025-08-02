import discord
from discord.ext import commands

ROLES_BY_LEVEL = {
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
    50: "👑 Lãnh đạo tối cao"
}

def get_level_role(level):
    levels = sorted(ROLES_BY_LEVEL.keys())
    role_name = ROLES_BY_LEVEL[1]  # Default role
    for lvl in levels:
        if level >= lvl:
            role_name = ROLES_BY_LEVEL[lvl]
    return role_name

async def update_user_role(member, level):
    """Update user's role based on their level"""
    try:
        print(f"[DEBUG] Gán role cho {member.display_name} với cấp {level}")

        guild = member.guild
        target_role_name = get_level_role(level)

        # Find the target role
        target_role = discord.utils.get(guild.roles, name=target_role_name)
        if not target_role:
            print(f"Role '{target_role_name}' not found in guild")
            return

        print(f"[CHECK] Bot's top role: {guild.me.top_role}, Role to assign: {target_role}")

        # Remove old level roles
        roles_to_remove = []
        for role in member.roles:
            if role.name in ROLES_BY_LEVEL.values() and role != target_role:
                roles_to_remove.append(role)

        if roles_to_remove:
            await member.remove_roles(*roles_to_remove)

        # Add new role if not already present
        if target_role not in member.roles:
            await member.add_roles(target_role)
            print(f"[INFO] Đã gán role: {target_role.name} cho {member.display_name}")

    except Exception as e:
        print(f"Error updating role for {member}: {e}")

class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(RoleManager(bot))