import discord
from discord.ext import commands
from utils.xp_manager import load_data, save_data
from cogs.role_manager import update_user_role

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlevel(self, ctx, member: discord.Member, level: int):
        data = load_data()
        user_id = str(member.id)
        if user_id not in data:
            data[user_id] = {"xp": 0, "level": 1}
        data[user_id]["level"] = level
        data[user_id]["xp"] = 0
        save_data(data)

        await update_user_role(member, level)
        await ctx.send(f"✅ Đã đặt level {level} cho {member.display_name} và cập nhật role.")

async def setup(bot):
    await bot.add_cog(Admin(bot))