import csv
import sqlite3

DB_PATH = 'data/app.db'
CSV_PATH = 'data/dishes.csv'

def insert_dishes_from_csv():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        with open(CSV_PATH, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                try:
                    cursor.execute('''
                        INSERT INTO Dishes (
                            dish_name,
                            dietary_restrictions,
                            health_goals,
                            meal_type,
                            time_to_prepare,
                            ingredient_availability,
                            cooking_equipment,
                            budget,
                            occasion,
                            taste_preferences,
                            sustainability
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row['dish_name'],
                        row['dietary_restrictions'],
                        row['health_goals'],
                        row['meal_type'],
                        row['time_to_prepare'],
                        row['ingredient_availability'],
                        row['cooking_equipment'],
                        row['budget'],
                        row['occasion'],
                        row['taste_preferences'],
                        row['sustainability']
                    ))
                except sqlite3.IntegrityError as e:
                    print(f"Skipping duplicate entry for {row['dish_name']}: {e}")
            conn.commit()
    print("Data insertion completed.")

def create_tables():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                google_id TEXT UNIQUE NOT NULL,
                email TEXT,
                name TEXT
            )
        ''')
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserSelections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                dish_id INTEGER NOT NULL,
                rating INTEGER,  -- Allow NULL for rating
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(id),
                FOREIGN KEY (dish_id) REFERENCES Dishes(id)
            )
        ''')
        conn.commit()