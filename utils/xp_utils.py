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

def get_xp_for_next_level(level):
  return get_needed_xp(level + 1)

def get_role_for_level(level):
  role_info = get_level_role(level)
  if role_info:
      return {"icon": role_info[0], "name": role_info[1]}
  return {"icon": "🧍‍♂️", "name": "Dân thường"}

def get_rank(user_id):
  from utils.data_manager import read_json
  
  user_data = read_json("data/user_data.json")
  if not user_data:
      return 1, 1
  
  # Tạo danh sách user và XP để sắp xếp
  user_list = []
  for uid, data in user_data.items():
      xp = data.get("xp", 0)
      user_list.append((uid, xp))
  
  # Sắp xếp theo XP giảm dần
  user_list.sort(key=lambda x: x[1], reverse=True)
  
  # Tìm vị trí của user
  for i, (uid, xp) in enumerate(user_list):
      if uid == user_id:
          return i + 1, len(user_list)
  
  return len(user_list), len(user_list)