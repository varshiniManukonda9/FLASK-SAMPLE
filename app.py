from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from passlib.hash import sha256_crypt

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key_here'

# MongoDB connection setup
client = MongoClient("127.0.0.1:27017")  # Use your MongoDB URI
db = client['flask_db']  # Database name
users_collection = db['users']  # Collection for user data

# Home route
@app.route('/')
def home():
    return render_template('login.html')

# Register route (for simplicity)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password
        hashed_password = sha256_crypt.hash(password)

        # Store user in MongoDB
        users_collection.insert_one({'username': username, 'password': hashed_password})

        flash("Registration Successful!", "success")
        return redirect(url_for('home'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if user exists
    user = users_collection.find_one({'username': username})
    
    if user and sha256_crypt.verify(password, user['password']):
        flash("Login Successful!", "success")
        return redirect(url_for('home'))
    else:
        flash("Invalid Username or Password!", "danger")
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

