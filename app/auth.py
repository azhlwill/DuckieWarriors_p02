# TNPG: DuckieWarriors
# Roster: Cody, James, William

import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_FILE = os.path.join(BASE_DIR, "database.db")


def login(username, password):
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute(
            "SELECT password FROM users WHERE username = ?",
            (username,)
        )
        row = c.fetchone()
        return row is not None and row[0] == password


def register(username, password):
    if not username or not password:
        return "Missing username or password"

    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()

        c.execute(
            "SELECT 1 FROM users WHERE username = ?",
            (username,)
        )
        if c.fetchone():
            return "Username already exists"

        c.execute(
            "INSERT INTO users VALUES (?, ?)",
            (username, password)
        )
        db.commit()

    return "Registered"
