# TNPG: DuckieWarriors
# Roster: Cody, James, William

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "database.db")


def build():
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()

        c.executescript("""
        DROP TABLE IF EXISTS favorites;
        DROP TABLE IF EXISTS recipes;
        DROP TABLE IF EXISTS users;

        CREATE TABLE users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        );

        CREATE TABLE recipes (
            recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_username TEXT,
            title TEXT,
            ingredients TEXT,
            instructions TEXT,
            image_url TEXT,
            calories INTEGER
        );

        CREATE TABLE favorites (
            username TEXT,
            recipe_id INTEGER,
            FOREIGN KEY(username) REFERENCES users(username),
            FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id)
        );
        """)

        c.execute("INSERT INTO users VALUES ('Admin', 'admin')")

        recipes = [
            ("Admin", "Midnight Grilled Cheese", "Bread, Cheese, Butter", "Butter bread, grill until golden.", "", 420),
            ("Admin", "Lazy Ramen Boost", "Ramen, Egg, Scallions", "Boil ramen, crack egg, stir.", "", 380),
            ("Admin", "Crispy Breakfast Potatoes", "Potatoes, Oil, Salt", "Pan fry until crispy.", "", 450),
            ("Admin", "Protein Scramble", "Eggs, Spinach, Cheese", "Scramble everything together.", "", 390),
            ("Admin", "Dorm Room Quesadilla", "Tortilla, Cheese", "Heat tortilla, melt cheese.", "", 340),
            ("Admin", "Late-Night Fried Rice", "Rice, Egg, Soy Sauce", "Stir fry all ingredients.", "", 500),
            ("Admin", "Simple Tomato Toast", "Bread, Tomato, Olive Oil", "Toast bread, add tomato.", "", 310),
            ("Admin", "Peanut Butter Banana", "Banana, Peanut Butter", "Spread and eat.", "", 290),
            ("Admin", "Microwave Mug Omelet", "Eggs, Milk, Cheese", "Microwave until set.", "", 360),
            ("Admin", "One-Pot Pasta", "Pasta, Garlic, Olive Oil", "Boil everything together.", "", 470),
            ("Admin", "Honey Garlic Chicken", "Chicken, Honey, Garlic", "Bake until cooked.", "", 520),
            ("Admin", "Quick Chili Bowl", "Beans, Ground Beef, Chili Powder", "Simmer for 20 minutes.", "", 560),
            ("Admin", "Pan-Seared Salmon", "Salmon, Salt, Pepper", "Sear skin-side down.", "", 510),
            ("Admin", "Veggie Stir Fry", "Mixed Veggies, Soy Sauce", "High heat stir fry.", "", 430),
            ("Admin", "Baked Ziti Shortcut", "Pasta, Marinara, Cheese", "Bake until bubbly.", "", 580),
            ("Admin", "Apple Cinnamon Oatmeal", "Oats, Apple, Cinnamon", "Cook oats, add apple.", "", 330),
            ("Admin", "Yogurt Berry Bowl", "Yogurt, Berries, Honey", "Mix together.", "", 300),
            ("Admin", "Chocolate Milkshake", "Milk, Ice Cream", "Blend until smooth.", "", 600),
            ("Admin", "Frozen Fruit Smoothie", "Frozen Fruit, Juice", "Blend.", "", 280),
            ("Admin", "Energy Peanut Balls", "Peanut Butter, Oats, Honey", "Roll into balls.", "", 350)
        ]

        c.executemany("""
            INSERT INTO recipes
            (author_username, title, ingredients, instructions, image_url, calories)
            VALUES (?, ?, ?, ?, ?, ?)
        """, recipes)

        db.commit()

    print("Database rebuilt with many recipes.")


if __name__ == "__main__":
    build()
