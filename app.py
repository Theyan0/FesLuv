from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flash messages

# MongoDB Configuration
client = MongoClient("mongodb+srv://admin:!Kyawkyaw1986@bustech.e03j1dn.mongodb.net/")
db = client['Hackathon']
users_collection = db["Users"]  # Collection Name

@app.route('/')
def index():
    return redirect(url_for('signup'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        age = request.form.get("age")
        password = request.form.get("password")

        # Input validation
        if not name or not email or not age or not password:
            flash("All fields are required!", "error")
            return redirect(url_for('signup'))
        
        # Check age
        if int(age) < 18:
            flash("You must be at least 18 years old to join us.", "error")
            return redirect(url_for('signup'))
        
        # Check for existing user
        if users_collection.find_one({"email": email}):
            flash("Email already registered!", "error")
            return redirect(url_for('signup'))
        
        # Insert into MongoDB
        users_collection.insert_one({
            "name": name,
            "email": email,
            "age": age,
            "password": password  # Consider hashing passwords
        })
        
        flash("Signup successful!", "success")
        return redirect(url_for('signup'))
    
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
    