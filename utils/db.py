import sqlite3

DB_PATH = 'data/app.db'

def create_tables():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        # Dishes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Dishes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dish_name TEXT UNIQUE NOT NULL,
                dietary_restrictions TEXT,
                health_goals TEXT,
                meal_type TEXT,
                time_to_prepare TEXT,
                ingredient_availability TEXT,
                cooking_equipment TEXT,
                budget TEXT,
                occasion TEXT,
                taste_preferences TEXT,
                sustainability TEXT
            )
        ''')
        # UserSelections table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserSelections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                dish_id INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(id),
                FOREIGN KEY (dish_id) REFERENCES Dishes(id)
            )
        ''')
        conn.commit()