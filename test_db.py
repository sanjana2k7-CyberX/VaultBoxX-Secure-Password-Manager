from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["vaultboxx"]
collection = db["credentials"]

result = collection.insert_one({
    "website": "gmail.com",
    "username": "test@gmail.com",
    "password": "encrypted_password"
})

print("Inserted ID:", result.inserted_id)