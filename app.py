from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, flash, session
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flash messages

# MongoDB Configuration
client = MongoClient("mongodb+srv://admin:!Kyawkyaw1986@bustech.e03j1dn.mongodb.net/")
db = client['Hackathon']
users_collection = db["Users"]  # Collection Name
receivers_collection = db["Receivers"]  # Replace with your collection name

# Hardcoded list of 100 items for the wishlist
ITEMS_LIST = [
    "Book", "Coffee Mug", "Socks", "Candles", "Puzzle", "Pen Set", "Journal", 
    "Keychain", "Plant Pot", "Scarf", "Chocolate Box", "Notebook", "Headphones", 
    "T-Shirt", "Water Bottle", "Fridge Magnets", "Lip Balm", "Hand Cream", 
    "Stickers", "Bookmark"
]

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
            session["user"] = user["name"]  # Store username in session
            flash("Login successful! Welcome, {}.".format(user["name"]), "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password. Please try again or sign up.", "error")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/secretsanta', methods=['GET', 'POST'])
def secretsanta_logged_in():
    if "user" not in session:
        flash("Please log in to access Secret Santa.", "error")
        return redirect(url_for('login'))

    username = session["user"]

    # Check if the user already has a wishlist and a receiver assigned
    user_data = users_collection.find_one({"name": username})

    if request.method == 'POST':
        # Save the selected wishlist items and assign a receiver
        selected_items = request.form.getlist("wishlist_items")

        if len(selected_items) != 10:
            flash("Please select exactly 10 items for your wishlist.", "error")
            return redirect(url_for('secretsanta_logged_in'))

        # Randomly assign a receiver
        receivers = list(receivers_collection.find({}))
        selected_receiver = random.choice(receivers)

        # Update user data with wishlist and receiver
        users_collection.update_one(
            {"name": username},
            {"$set": {
                "wishlist": selected_items,
                "receiver": {
                    "ReceiverName": selected_receiver['ReceiverName'],
                    "Wishlist": selected_receiver['Wishlist']
                }
            }}
        )

        flash("Wishlist saved and receiver assigned!", "success")
        return redirect(url_for('secretsanta_logged_in'))

    # Check if the user already has a receiver and wishlist
    if user_data and "wishlist" in user_data and "receiver" in user_data:
        return render_template(
            'secretsanta.html',
            username=username,
            items_list=ITEMS_LIST,
            receiver_name=user_data['receiver']['ReceiverName'],
            receiver_wishlist=user_data['receiver']['Wishlist'],
            user_wishlist=user_data['wishlist']
        )
    else:
        # First-time users need to select their wishlist
        return render_template(
            'wishlist_form.html',
            username=username,
            items_list=ITEMS_LIST
        )

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

@app.route("/volunteer")
def volunteer():
    return render_template("volunteer.html")

@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
