import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone
from utils import xp_manager

class XPReset(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_reset.start()

    def cog_unload(self):
        self.daily_reset.cancel()

    @tasks.loop(minutes=5)  # Kiểm tra mỗi 5 phút
    async def daily_reset(self):
        now = datetime.utcnow()
        if now.hour == 0 and now.minute < 5:  # 0h UTC = 7h sáng Việt Nam
            print("[XP RESET] Đang reset daily XP...")
            xp_manager.reset_all_user_daily_data()

    @daily_reset.before_loop
    async def before_reset(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(XPReset(bot))