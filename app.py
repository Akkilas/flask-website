from flask import Flask, g
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'database.db'


def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')

@app.before_first_request
def initialize():
    init_db()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_FILE)
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db:
        db.close()


@app.route('/')
def home():
    return '✅ Flask app is running on Render with SQLite DB!'


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
