import sqlite3

# 创建数据库连接和游标
conn = sqlite3.connect('preferences.db')
cursor = conn.cursor()

# 创建表格
cursor.execute('''
CREATE TABLE IF NOT EXISTS UserPreferences (
    user_id TEXT PRIMARY KEY,
    preferences TEXT
)
''')

# 插入用户口味信息
def add_user_preference(user_id, preferences):
    # 将字典转换为字符串
    preferences_str = str(preferences)
    cursor.execute('''
    INSERT OR REPLACE INTO UserPreferences (user_id, preferences)
    VALUES (?, ?)
    ''', (user_id, preferences_str))
    conn.commit()

# 获取用户口味信息
def get_user_preference(user_id):
    cursor.execute('''
    SELECT preferences FROM UserPreferences WHERE user_id = ?
    ''', (user_id,))
    result = cursor.fetchone()
    if result:
        return eval(result[0])  # 将字符串转换回字典
    else:
        return None

# 示例添加和读取
preferences = {
    'sweet': 0.8,
    'sour': 0.3,
    'bitter': 0.1,
    'salty': 0.5
}

add_user_preference('user_123', preferences)

# 获取用户口味信息
user_preferences = get_user_preference('user_123')
print(user_preferences)

# 关闭连接
conn.close()
