import discord
from discord.ext import commands, tasks
from utils.data_manager import read_json, write_json
from utils.xp_utils import get_level, get_needed_xp, get_rank, get_level_role
from datetime import datetime, timezone
import asyncio

GUILD_ID = 1384239080937754714  # ❗ Thay bằng ID server thật
ANNOUNCE_CHANNEL_ID = 1401071206219776092  # ❗ Thay bằng ID kênh thông báo

class XPTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_check.start()

    def cog_unload(self):
        self.daily_check.cancel()

    @tasks.loop(minutes=1)
    async def daily_check(self):
        now = datetime.now(timezone.utc)
        if now.hour == 0 and now.minute == 0:  # 00:00 UTC
            await self.handle_daily_reset()

    async def handle_daily_reset(self):
        await self.bot.wait_until_ready()

        guild = self.bot.get_guild(GUILD_ID)
        channel = guild.get_channel(ANNOUNCE_CHANNEL_ID)
        if not guild or not channel:
            print("❌ Không tìm thấy guild hoặc channel.")
            return

        user_data = read_json("data/user_data.json")
        msg_data = read_json("data/xp_messages.json")  # File đếm số tin nhắn
        log = []

        for uid, data in user_data.items():
            member = guild.get_member(int(uid))
            if not member:
                continue

            old_level = get_level(data["xp"])
            msg_count = msg_data.get(uid, 0)

            # Người không đủ 10 tin → trừ XP + tụt role
            if msg_count < 10:
                data["xp"] = max(0, data["xp"] - 50)
                new_level = get_level(data["xp"])
                log.append(f"🔻 {member.mention} không hoàn thành nhiệm vụ (gửi {msg_count}/10 tin) → -50 XP.")

                if new_level < old_level:
                    old_role = get_level_role(old_level)
                    new_role = get_level_role(new_level)

                    if old_role:
                        role_obj = discord.utils.get(guild.roles, name=old_role[1])
                        if role_obj in member.roles:
                            await member.remove_roles(role_obj)

                    if new_role:
                        role_obj = discord.utils.get(guild.roles, name=new_role[1])
                        await member.add_roles(role_obj)

            # Người vừa đạt mốc level → gán role mới
            else:
                new_level = get_level(data["xp"])
                if new_level > old_level and new_level % 5 == 0:
                    role_info = get_level_role(new_level)
                    if role_info:
                        role_obj = discord.utils.get(guild.roles, name=role_info[1])
                        if role_obj:
                            await member.add_roles(role_obj)
                            log.append(f"🔺 {member.mention} đã đạt cấp {new_level} → cấp vai trò {role_info[1]}.")

        # Ghi lại data và reset đếm tin nhắn
        write_json("data/user_data.json", user_data)
        write_json("data/xp_messages.json", {})

        # Gửi log thông báo
        if log:
            embed = discord.Embed(title="📅 Tổng kết nhiệm vụ hàng ngày", description="\n".join(log), color=0x00ff99)
            await channel.send(embed=embed)
        else:
            await channel.send("📅 Hôm nay không có thay đổi nào về XP hoặc role.")

    @daily_check.before_loop
    async def before_task(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(XPTasks(bot))