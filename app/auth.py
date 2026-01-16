# TNPG: DuckieWarriors
# Roster: Cody, James, William

import sqlite3

DB_FILE = "database.db"

def login(username, password):
    """
    Checks if the username and password match a record in the database.
    Returns True if valid, False otherwise.
    """
    try:
        with sqlite3.connect(DB_FILE) as db:
            c = db.cursor()
            c.execute("SELECT password FROM users WHERE username = ?", (username,))
            result = c.fetchone()
            
            if result and result[0] == password:
                return True
            return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

def register(username, password):
    """
    Attempts to add a new user.
    Returns 'Registered' on success, or an error message on failure.
    """
    try:
        with sqlite3.connect(DB_FILE) as db:
            c = db.cursor()

            c.execute("SELECT username FROM users WHERE username = ?", (username,))
            if c.fetchone():
                return "Username taken"
            
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            return "Registered"
    except sqlite3.Error:
        return "Database Error"
