# TNPG: DuckieWarriors
# Roster: Cody, James, William

from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os
import auth
import build_db

app = Flask(__name__)
app.secret_key = os.urandom(32)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "database.db")

if not os.path.exists(DB_FILE):
    build_db.build()


@app.route("/", methods=["GET", "POST"])
def home():
    if "username" in session:
        return redirect(url_for("game"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if auth.login(username, password):
            session["username"] = username
            return redirect(url_for("game"))
        else:
            return render_template("home.html", error="Invalid login")

    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        result = auth.register(username, password)
        if result == "Registered":
            session["username"] = username
            return redirect(url_for("game"))
        else:
            return render_template("register.html", error=result)

    return render_template("register.html")


@app.route("/game")
def game():
    if "username" not in session:
        return redirect(url_for("home"))
    return render_template("game.html", user=session["username"])


@app.route("/unlock_recipe")
def unlock_recipe():
    if "username" not in session:
        return redirect(url_for("home"))

    username = session["username"]

    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()

        c.execute("SELECT * FROM recipes ORDER BY RANDOM() LIMIT 1")
        recipe = c.fetchone()

        if recipe:
            recipe_id = recipe[0]

            c.execute("""
                SELECT 1 FROM favorites
                WHERE username = ? AND recipe_id = ?
            """, (username, recipe_id))

            if not c.fetchone():
                c.execute("""
                    INSERT INTO favorites (username, recipe_id)
                    VALUES (?, ?)
                """, (username, recipe_id))
                db.commit()

            return render_template("recipe.html", recipe=recipe)

    return "No recipes found."


@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect(url_for("home"))

    username = session["username"]

    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute("""
            SELECT recipes.title, recipes.ingredients,
                   recipes.instructions, recipes.calories
            FROM recipes
            JOIN favorites ON recipes.recipe_id = favorites.recipe_id
            WHERE favorites.username = ?
        """, (username,))
        recipes = c.fetchall()

    return render_template("profile.html", user=username, recipes=recipes)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
