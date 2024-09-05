from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Exercice 1 : 

def create_award_year_index(client: MongoClient) -> str:
    index_name = client["nobel"]["laureates"].create_index(
        [("prizes.year", -1)]
    )
    
    return index_name

def get_laureates_year(client: MongoClient, year: int) -> list[dict]:
    results = client["nobel"]["laureates"].find(
        {"prizes.year": year},
        {"_id": 0, "firstname": 1, "surname": 1, "prizes.year": 1}
    )
    
    return list(results)

# Exercice 2 :

def create_country_index(client: MongoClient) -> str:
    index_name = client["nobel"]["laureates"].create_index(
        [("bornCountry", "text"), ("diedCountry", "text")]
    )
    return index_name

def get_country_laureates(client: MongoClient, country: str) -> list[dict]:
    results = client["nobel"]["laureates"].find(
        {"$text": {"$search": country}},
        {"_id": 0, "firstname": 1, "surname": 1, "bornCountry": 1, "diedCountry": 1}
    )
    return list(results)

# Exercice 3 :

def create_gender_category_index(client: MongoClient) -> str:
    index_name = client["nobel"]["laureates"].create_index(
        [("prizes.category", -1), ("gender", 1)]
    )
    return index_name

def get_gender_category_laureates(client: MongoClient, gender: str, category: str) -> list[dict]:
    results = client["nobel"]["laureates"].find(
        {"gender": gender, "prizes.category": category},
        {"_id": 0, "firstname": 1, "surname": 1, "gender": 1, "prizes.category": 1}
    )
    return list(results)

# Exercice 4 :

def create_year_category_index(client: MongoClient) -> str:
    index_name = client["nobel"]["prizes"].create_index(
        [("year", 1), ("category", 1)],
        unique=True
    )
    return index_name
