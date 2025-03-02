from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def create_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS users")
    c.execute('''CREATE TABLE users (username TEXT, password TEXT)''')
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'ZZZZZ')")
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('welcome'))
        else:
            return "Login Failed! Try Again."
    return render_template("login.html")  # تم استبدال HTML المدمج بملف خارجي

@app.route('/welcome')
def welcome():
    if 'logged_in' in session:
        return f"Welcome {session['username']}! You have successfully logged in."
    return redirect(url_for('login'))

if __name__ == '__main__':
    create_database()
    app.run()
