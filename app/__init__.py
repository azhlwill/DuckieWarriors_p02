# TNPG: DuckieWarriors
# Roster: Cody, James, William

from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import auth

app = Flask(__name__)
app.secret_key = 'super_secret_key' 

DB_FILE = "database.db"

@app.route("/", methods=["GET", "POST"])
def home():
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
        result = auth.register(username, password)
        if result == "Registered":
            session["user_id"] = username
            return redirect(url_for("game"))
        else:
            return render_template("register.html", error=result)
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
        
    try:
        with sqlite3.connect(DB_FILE) as db:
            c = db.cursor()
            c.execute("SELECT * FROM recipes ORDER BY RANDOM() LIMIT 1")
            recipe = c.fetchone()
            
        if recipe:
            return render_template("recipe.html", recipe=recipe)
        else:
            return "No recipes found. Run build_db.py!"
    except sqlite3.Error as e:
        return f"Database Error: {e}"

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)