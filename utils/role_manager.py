async def update_user_role(user, new_level):
  guild = user.guild
  level_roles = {
      1: ("Dân thường", "🧍‍♂️", 0x808080),
      5: ("Tổ trưởng khu phố", "🌱", 0x2ecc71),
      10: ("Cán bộ xã", "🧑‍💼", 0x3498db),
      15: ("Chủ nhiệm CLB", "🎯", 0x9b59b6),
      20: ("Quận trưởng", "🏛️", 0xe67e22),
      25: ("Trưởng phòng tài chính", "💰", 0xf1c40f),
      30: ("Phó chủ tịch TP", "🏙️", 0x1abc9c),
      35: ("Bộ trưởng sự kiện", "🎉", 0xe84393),
      40: ("Đặc vụ XP", "⚔️", 0xc0392b),
      45: ("Thanh tra cấp cao", "🕵️‍♂️", 0x7f8c8d),
      50: ("Lãnh đạo tối cao", "👑", 0xf39c12)
  }

  # Tìm role cao nhất phù hợp với level hiện tại
  highest = max([lv for lv in level_roles if new_level >= lv], default=1)
  name, emoji, color = level_roles[highest]

  # Tạo role nếu chưa có
  role_name = f"{emoji} {name}"
  role = discord.utils.get(guild.roles, name=role_name)
  if role is None:
      role = await guild.create_role(
          name=role_name,
          color=discord.Color(color),
          reason="Tạo role cấp độ"
      )

  # Gỡ các role cấp độ cũ
  for lv, (rname, emoji_r, _) in level_roles.items():
      old_role = discord.utils.get(guild.roles, name=f"{emoji_r} {rname}")
      if old_role and old_role in user.roles:
          await user.remove_roles(old_role)

  # Gán role mới nếu chưa có
  if role not in user.roles:
      await user.add_roles(role)