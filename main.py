import re
import sqlite3
from flask import Flask, request, redirect, render_template,send_from_directory
import os
app = Flask(__name__)

conn = sqlite3.connect('data1.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS data1 (
             username text,
             password text,
             first_name text,
             last_name text,
             email text
             )""")
conn.commit()
conn.close()

@app.route('/', methods=['GET', 'POST'])
def register():
    message=None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        conn = sqlite3.connect('data1.db')
        c = conn.cursor()
        c.execute("INSERT INTO data1 (username, password,first_name,last_name,email) VALUES (?,?,?,?,?)",
                  (username, password,first_name,last_name,email))
        conn.commit()
        conn.close()
        message="Registration Successful.Please log in to continue"
        return redirect('/retrieve')
    return render_template('register.html',message=message)


@app.route('/retrieve', methods=['GET', 'POST'])
def retrieve():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('data1.db')
        c = conn.cursor()
        c.execute("SELECT * FROM data1 WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            return render_template('user.html',user=user)
        else:
            return "Incorrect username or password"
    return render_template('retrieve.html')

if __name__ == '__main__':
    app.run(debug=True)

