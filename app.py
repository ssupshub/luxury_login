from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config["MONGO_URI"] = "your_mongodb_connection_string"
mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = mongo.db.users.find_one({'username': username})

    if user and check_password_hash(user['password'], password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    return f"Welcome, {session['username']}!"

if __name__ == '__main__':
    app.run(debug=True)
