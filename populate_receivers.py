from pymongo import MongoClient

# MongoDB Configuration
client = MongoClient("mongodb+srv://admin:!Kyawkyaw1986@bustech.e03j1dn.mongodb.net/")
db = client['Hackathon']
receivers_collection = db["Receivers"]

# Sample Receiver Data
receivers_data = [
    {
        "ReceiverID": 1,
        "ReceiverName": "Alice",
        "Wishlist": ["Book", "Plant Pot", "Socks", "Candles", "Journal", "Chocolate Box", "Notebook", "Scarf", "Pen Set", "Lip Balm"]
    },
    {
        "ReceiverID": 2,
        "ReceiverName": "Bob",
        "Wishlist": ["Puzzle", "T-Shirt", "Water Bottle", "Keychain", "Fridge Magnets", "Headphones", "Notebook", "Bookmark", "Hand Cream", "Stickers"]
    },
    {
        "ReceiverID": 3,
        "ReceiverName": "Charlie",
        "Wishlist": ["Journal", "Book", "Candles", "Headphones", "Plant Pot", "Socks", "T-Shirt", "Water Bottle", "Chocolate Box", "Stickers"]
    },
    {
        "ReceiverID": 4,
        "ReceiverName": "David",
        "Wishlist": ["Keychain", "Puzzle", "Scarf", "Notebook", "Pen Set", "Hand Cream", "Lip Balm", "Chocolate Box", "Plant Pot", "Bookmark"]
    },
    {
        "ReceiverID": 5,
        "ReceiverName": "Emma",
        "Wishlist": ["Fridge Magnets", "Lip Balm", "Candles", "Notebook", "Puzzle", "Socks", "Scarf", "Water Bottle", "Keychain", "Headphones"]
    }
]

# Insert Data into MongoDB
receivers_collection.insert_many(receivers_data)
print("Receivers data successfully added to MongoDB!")
