# TNPG: DuckieWarriors
# Roster: Cody, James, William
# Description: Database setup and seeding

import sqlite3

DB_FILE = "database.db"

def create_tables():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    # Drop existing tables to reset
    c.execute("DROP TABLE IF EXISTS favorites")
    c.execute("DROP TABLE IF EXISTS recipes")
    c.execute("DROP TABLE IF EXISTS users")

    # USERS TABLE
    c.execute("""
        CREATE TABLE users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)

    # RECIPES TABLE
    c.execute("""
        CREATE TABLE recipes (
            recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_username TEXT,
            title TEXT NOT NULL,
            ingredients TEXT,
            instructions TEXT,
            image_url TEXT,
            calories INTEGER
        )
    """)

    # FAVORITES TABLE
    c.execute("""
        CREATE TABLE favorites (
            username TEXT,
            recipe_id INTEGER,
            FOREIGN KEY(username) REFERENCES users(username),
            FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id)
        )
    """)

    # SEED DATA
    seed_recipes(c)

    db.commit()
    db.close()
    print("Database built and seeded successfully.")

def seed_recipes(cursor):
    recipes = [
        ("Admin", "Victory Pancakes", "Flour, Milk, Eggs, Syrup", "1. Mix. 2. Fry. 3. Eat.", "https://placeholder.com/pancakes.jpg", 350),
        ("Admin", "Brain-Power Pasta", "Pasta, Tomato Sauce, Basil", "Boil water, cook pasta, add sauce.", "https://placeholder.com/pasta.jpg", 400),
        ("Admin", "Miner's Stew", "Beef, Potatoes, Carrots, Broth", "Slow cook for 6 hours.", "https://placeholder.com/stew.jpg", 550)
    ]
    
    cursor.executemany("""
        INSERT INTO recipes (author_username, title, ingredients, instructions, image_url, calories)
        VALUES (?, ?, ?, ?, ?, ?)
    """, recipes)

if __name__ == "__main__":
    create_tables()
