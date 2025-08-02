# This file is disabled to avoid conflicts with xp_cog.py
# The main XP system in xp_cog.py handles daily resets properly

# Original code commented out to prevent conflicts
# import discord
# from discord.ext import commands, tasks
# from datetime import datetime, timezone
# import json
#
# DATA_PATH = "data/user_data.json"
#
# def load_data():
#     try:
#         with open(DATA_PATH, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except:
#         return {}
#
# def save_data(data):
#     with open(DATA_PATH, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=2, ensure_ascii=False)
#
# class DailyReset(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.reset_daily_xp.start()
#
#     def cog_unload(self):
#         self.reset_daily_xp.cancel()
#
#     @tasks.loop(minutes=5)
#     async def reset_daily_xp(self):
#         now = datetime.utcnow()
#         # Reset lúc 0h UTC (7h VN)
#         if now.hour == 0 and now.minute < 5:
#             data = load_data()
#             changed_users = []
#             for user_id, user in data.items():
#                 daily_xp = user.get("dailyXP", 0)
#                 level = user.get("level", 1)
#                 xp = user.get("xp", 0)
#
#                 # Nếu chưa đạt 30 XP (quy định) thì trừ XP
#                 if daily_xp < 30 and level > 1:
#                     xp_to_subtract = int(0.05 * (xp + level * 100)) + level * 10
#                     user["xp"] = max(0, xp - xp_to_subtract)
#
#                 # Nếu XP tụt xuống dưới mốc, tụt cấp (giao cho cog leveling xử lý)
#                 # Ở đây ta chỉ chỉnh xp, phần tụt cấp sẽ tự động khi người dùng nhắn tin
#
#                 # Reset dailyXP và các trạng thái khác
#                 user["dailyXP"] = 0
#                 user["messages"] = 0
#                 user["lastMission"] = ""  # Reset để nhận lại mission
#                 user["dailyXPClaimed"] = False  # Cho phép nhận lại dailyxp
#                 changed_users.append(user_id)
#
#             save_data(data)
#             print(f"[Daily Reset] Đã reset dailyXP cho {len(changed_users)} user.")
#
#     @reset_daily_xp.before_loop
#     async def before_reset(self):
#         await self.bot.wait_until_ready()
#
# async def setup(bot):
#     await bot.add_cog(DailyReset(bot))

async def setup(bot):
    pass  # Don't load this cog