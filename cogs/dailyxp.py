import discord
from discord.ext import commands
from discord import app_commands
import jsonfrom datetime import datetime, timedelta

DATA_PATH = "data/user_data.json"

def load_data():
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
def save_data(data):
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def ensure_user_exists(user_id):
        data = load_data()
        user_id = str(user_id)
        if user_id not in data:
            data[user_id] = {
                "xp": 0,
                "level": 1,
                "daily_xp": 0,
                "lastDailyXP": None,
                "xpBoostExpire": None,
                "last_mission": None
            }
            save_data(data)
        return data

class DailyXP(commands.Cog):
        def __init__(self, bot):
            self.bot = bot

        @app_commands.command(name="dailyxp", description="Dùng 1 lần/ngày để tăng gấp đôi XP trong 1 giờ")
        async def dailyxp(self, interaction: discord.Interaction):
            user_id = str(interaction.user.id)
            now = datetime.utcnow()

            data = ensure_user_exists(user_id)
            user = data[user_id]

            last_used = user.get("lastDailyXP", None)
            if last_used:
                last_used_dt = datetime.fromisoformat(last_used)
                if last_used_dt.date() == now.date():
                    await interaction.response.send_message("📛 Bạn đã dùng lệnh này hôm nay rồi!", ephemeral=True)
                    return

            user["lastDailyXP"] = now.isoformat()
            user["xpBoostExpire"] = (now + timedelta(hours=1)).isoformat()
            save_data(data)

            await interaction.response.send_message("🎉 Bạn đã kích hoạt **x2 XP** trong 1 giờ!", ephemeral=True)

    # ✅ Phải có setup để load cog đúng
async def setup(bot):
        await bot.add_cog(DailyXP(bot))