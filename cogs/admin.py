
import discord
from discord.ext import commands
from utils.xp_manager import load_data, save_data, get_user_data, update_user_data
from utils.xp_utils import get_level

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlevel(self, ctx, member: discord.Member, level: int):
        """Set a user's level"""
        data = load_data()
        user_id = str(member.id)
        
        if user_id not in data:
            data[user_id] = {
                "xp": 0,
                "level": 1,
                "daily_messages": 0,
                "daily_bonus_claimed": False,
                "last_message_ts": 0,
                "last_reset_date": None
            }
        
        # Calculate XP needed for the specified level
        total_xp = 0
        for i in range(1, level):
            total_xp += (50 + i * 25)
        
        data[user_id]["level"] = level
        data[user_id]["xp"] = total_xp
        save_data(data)

        await ctx.send(f"✅ Đã đặt level {level} cho {member.display_name}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setxp(self, ctx, member: discord.Member, xp: int):
        """Set a user's XP"""
        data = load_data()
        user_id = str(member.id)
        
        if user_id not in data:
            data[user_id] = {
                "xp": 0,
                "level": 1,
                "daily_messages": 0,
                "daily_bonus_claimed": False,
                "last_message_ts": 0,
                "last_reset_date": None
            }
        
        data[user_id]["xp"] = xp
        data[user_id]["level"] = get_level(xp)
        save_data(data)

        await ctx.send(f"✅ Đã đặt {xp} XP cho {member.display_name}")

async def setup(bot):
    await bot.add_cog(Admin(bot))
