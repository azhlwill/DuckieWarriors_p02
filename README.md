# Duck/Kitchen Sweeper by DuckieWarriors

## ROSTER
- William Li (PM)
- Cody Wong
- James Sun
- Alexandru Cimpoiesu

---

## DESCRIPTION
Duck/Kitchen Sweeper is a web-based Minesweeper-style game with a culinary theme. Users can register for an account, log in, and play a grid-based Minesweeper game. Successfully clearing the board unlocks a random recipe.

Unlocked recipes are permanently saved to the user’s profile and persist across sessions. Users can view all collected recipes on their profile page. The project demonstrates user authentication, database persistence, game logic, and dynamic page rendering using Flask and SQLite.

A developer shortcut is included to instantly unlock recipes for testing purposes.

---

## INSTALL GUIDE

### Pre-requisites
- Python 3 installed
- Git installed

---

## Clone the repository
```bash
git clone <your-repo-link-here>
cd DuckieWarriors_p02

mac/linux
python3 -m venv venv
source venv/bin/activate

windows
python -m venv venv
venv\Scripts\activate

install requirements
pip install -r requirements.txt

run app
cd app
python3 __init__.py

open link
http://127.0.0.1:5000
