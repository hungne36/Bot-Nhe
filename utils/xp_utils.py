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
  remaining_xp = xp
  while remaining_xp >= (50 + level * 25):
      remaining_xp -= (50 + level * 25)
      level += 1
  return level

def get_needed_xp(level):
  return 50 + level * 25

def get_level_role(level):
  keys = sorted(LEVEL_ROLES.keys(), reverse=True)
  for k in keys:
      if level >= k:
          return LEVEL_ROLES[k]
  return None

def get_xp_for_next_level(level):
    return 100 + level * 100  # hoặc công thức bạn đã dùng để tăng độ khó

def get_role_for_level(level):
  role_info = get_level_role(level)
  if role_info:
      return {"icon": role_info[0], "name": role_info[1]}
  return {"icon": "🧍‍♂️", "name": "Dân thường"}

def get_rank(user_id):
    from utils.data_manager import read_json
    
    data = read_json("data/user_data.json")
    rankings = sorted(data.items(), key=lambda x: x[1].get("xp", 0), reverse=True)
    total = len(rankings)
    for index, (uid, _) in enumerate(rankings, start=1):
        if uid == str(user_id):
            return index, total
    return total, total  # fallback nếu không tìm thấy