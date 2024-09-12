from pymongo import MongoClient
from bson import ObjectId

# Exercice 1 :

def add_laureate(client: MongoClient, laureate: dict) -> ObjectId:
    result = client["nobel"]["laureates"].insert_one(laureate)
    return result.inserted_id

# Exercice 2 :

def add_prizes(client: MongoClient, prize: dict) -> list[ObjectId]:
    result = client["nobel"]["prizes"].insert_one(prize)
    return result.inserted_id

# Exercice 3 :

def update_laureate(client: MongoClient, doc_id: ObjectId, dod: str, country: str, city: str) -> (int, int):
    result = client["nobel"]["laureates"].update_one(
        {"_id": doc_id},
        {"$set": {
            "died": dod,
            "diedCountry": country,
            "diedCity": city
        }}
    )
    return result.matched_count, result.modified_count

# Exercice 4 :

def upper_categories(client: MongoClient) -> (int, int):
    result = client["nobel"]["prizes"].update_many(
        {},
        [{"$set": {"category": {"$toUpper": "$category"}}}]
    )
    return result.matched_count, result.modified_count

# Exercice 5 :

def delete_prize(client: MongoClient, prize_id: ObjectId) -> (int, int):
    count_before = client["nobel"]["prizes"].count_documents({"_id": prize_id})
    result = client["nobel"]["prizes"].delete_one({"_id": prize_id})
    return count_before, result.deleted_count

# Exercice 6 :

def delete_laureates(client: MongoClient, dob: str) -> (int, int):
    count_before = client["nobel"]["laureates"].count_documents({"born": {"$lt": dob}})
    result = client["nobel"]["laureates"].delete_many({"born": {"$lt": dob}})
    return count_before, result.deleted_count