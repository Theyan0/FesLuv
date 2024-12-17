from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flash messages

# MongoDB Configuration
client = MongoClient("mongodb+srv://admin:!Kyawkyaw1986@bustech.e03j1dn.mongodb.net/")
db = client['Hackathon']
users_collection = db["Users"]  # Collection Name
@app.route('/')
def index():
    return render_template('index.html')  # Default page with Login/Signup buttons

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        age = request.form.get("age")
        password = request.form.get("password")

        if not name or not email or not age or not password:
            flash("All fields are required!", "error")
            return redirect(url_for('signup'))

        if int(age) < 18:
            flash("You must be at least 18 years old to join us.", "error")
            return redirect(url_for('signup'))

        if users_collection.find_one({"email": email}):
            flash("Email already registered! Please log in.", "error")
            return redirect(url_for('login'))

        users_collection.insert_one({
            "name": name,
            "email": email,
            "age": age,
            "password": password
        })

        flash("Signup successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = users_collection.find_one({"email": email, "password": password})
        if user:
            session["user"] = user["name"]
            flash("Login successful! Welcome, {}.".format(user["name"]), "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password. Please try again or sign up.", "error")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/home')
def home():
    if "user" in session:
        return render_template('home.html', user=session["user"])
    else:
        flash("Please log in to access the Home Page.", "error")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
    