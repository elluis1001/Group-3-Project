import sqlite3
import random
from flask import Flask, abort, session, render_template, request, g

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>EV Stations</h1>"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('california2.db')
        cursor = db.cursor()
        cursor.execute("SELECT station_name FROM California")
        all_data = cursor.fetchall()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    conn = get_db()
    posts = conn.execute('SELECT California FROM main_posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run()