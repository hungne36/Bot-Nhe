LEVEL_ROLES = {
  1: ("🧍‍♂️", "Dân thường"),
  5: ("🌱", "Người mới nổi"),
  10: ("🧑‍💼", "Cán bộ xã"),
  15: ("🎯", "Chủ nhiệm CLB"),
  20: ("🏛️", "Quận trưởng"),
  25: ("💰", "Trưởng phòng tài chính"),
  30: ("🏙️", "Phó chủ tịch TP"),
  35: ("🎉", "Bộ trưởng sự kiện"),
  40: ("⚔️", "Đặc vụ XP"),
  45: ("🕵️‍♂️", "Thanh tra cấp cao"),
  50: ("👑", "Lãnh đạo tối cao"),
}

def get_level(xp):
  level = 1
  while xp >= get_needed_xp(level + 1):
      level += 1
  return level

def get_needed_xp(level):
  return 100 * level + 1000

def get_level_role(level):
  keys = sorted(LEVEL_ROLES.keys(), reverse=True)
  for k in keys:
      if level >= k:
          return LEVEL_ROLES[k]
  return None