from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["vaultboxx"]
collection = db["credentials"]

def add_credential(website, username, password):
    collection.insert_one({
        "website": website,
        "username": username,
        "password": password
    })

def get_credentials():
    return list(collection.find())

def delete_credential(website):
    result = collection.delete_one(
        {"website": website}
    )

    return result.deleted_count

def search_credential(website):
    return collection.find_one(
        {"website": website}
    )