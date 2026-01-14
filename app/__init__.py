# TNPG: DuckieWarriors
# Roster: Cody, James, William

from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import auth
import build_db

app = Flask(__name__)
app.secret_key = 'super_secret_key' # Replace with valid key

DB_FILE = "database.db"

@app.route("/", methods=["GET", "POST"])
def home():
    # If user is logged in, send them to game
    if "user_id" in session:
        return redirect(url_for("game"))
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if auth.login(username, password):
            session["user_id"] = username
            return redirect(url_for("game"))
        else:
            return render_template("home.html", error="Invalid login.")
            
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if auth.register(username, password) == "Registered":
            session["user_id"] = username
            return redirect(url_for("game"))
        else:
            return render_template("register.html", error="Username taken or invalid.")
    return render_template("register.html")

@app.route("/game")
def game():
    if "user_id" not in session:
        return redirect(url_for("home"))
    return render_template("game.html", user=session["user_id"])

@app.route("/unlock_recipe")
def unlock_recipe():
    if "user_id" not in session:
        return redirect(url_for("home"))
        
    # User won! Fetch a random recipe
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM recipes ORDER BY RANDOM() LIMIT 1")
    recipe = c.fetchone()
    db.close()
    
    if recipe:
        return render_template("recipe.html", recipe=recipe)
    else:
        return "No recipes found. Run build_db.py!"

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
