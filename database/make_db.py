import sqlite3

conn = sqlite3.connect('preferences.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS UserPreferences (
    user_id TEXT PRIMARY KEY,
    preferences TEXT
)
''')

def add_user_preference(user_id, preferences):
    preferences_str = str(preferences)
    cursor.execute('''
    INSERT OR REPLACE INTO UserPreferences (user_id, preferences)
    VALUES (?, ?)
    ''', (user_id, preferences_str))
    conn.commit()

def get_user_preference(user_id):
    cursor.execute('''
    SELECT preferences FROM UserPreferences WHERE user_id = ?
    ''', (user_id,))
    result = cursor.fetchone()
    if result:
        return eval(result[0].replace('inf', 'float("inf")'))  
    else:
        return None

def update_user_preference(user_id, preferences):
    preferences_str = str(preferences)
    cursor.execute('''
    UPDATE UserPreferences SET preferences = ?
    WHERE user_id = ?
    ''', (preferences_str, user_id))
    conn.commit()

def delete_user_preference(user_id):
    cursor.execute('''
    DELETE FROM UserPreferences WHERE user_id = ?
    ''', (user_id,))
    conn.commit()

preferences = {
    'taste_preferences': {
        'sweet': 0.8,
        'sour': 0.3,
        'bitter': 0.1,
        'salty': 0.5,
        'umami': 0.7
    },
    'allergen_sensitivity': {
        'peanut': float('-inf'), 
        'gluten': 0.2,
        'dairy': 0.1,
        'soy': 0.5,
        'shellfish': float('-inf')
    },
    'ingredient_preferences': {
        'chocolate': 0.9,
        'coffee': 0.6,
        'vanilla': 0.8,
        'mint': 0.4,
        'cinnamon': 0.7
    }
}

add_user_preference('user_123', preferences)

print("Initial:", get_user_preference('user_123'))


new_preferences = {
    'taste_preferences': {
        'sweet': 0.6,
        'sour': 0.4,
        'bitter': 0.3,
        'salty': 0.7,
        'umami': 0.6
    },
    'allergen_sensitivity': {
        'peanut': float('-inf'),
        'gluten': 0.1,
        'dairy': 0.3,
        'soy': 0.4,
        'shellfish': float('-inf')
    },
    'ingredient_preferences': {
        'chocolate': 0.8,
        'coffee': 0.5,
        'vanilla': 0.9,
        'mint': 0.3,
        'cinnamon': 0.6
    }
}
update_user_preference('user_123', new_preferences)
print("Updated:", get_user_preference('user_123'))

delete_user_preference('user_123')
print("Deleted:", get_user_preference('user_123'))

conn.close()

