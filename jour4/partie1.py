from pymongo import MongoClient

# Exercice 1 :

def get_mongo_client(host:str, port:int) -> MongoClient:
    return MongoClient(host, port)

# Exercice 2 :

def get_all_laureates(client:MongoClient) -> list:
    return list(client["nobel"]["laureates"].find())

# Exercice 3 :

def get_laureates_information(client: MongoClient) -> list[dict]:
    return list(client["nobel"]["laureates"].find({}, {"firstname": 1, "surname": 1, "born": 1}))

def get_prize_categories(client: MongoClient) -> list[str]:
    return list(client["nobel"]["laureates"].distinct("prizes.category"))

# Exercice 4 :

def get_category_laureates(client: MongoClient, category: str) -> list[dict]:
    results = client["nobel"]["laureates"].find({"prizes.0.category": category}, {"_id": 0, "firstname": 1, "surname": 1, "category": 1})
    laureates = []
    for result in results:
        laureates.append({
            "firstname": result.get("firstname"),
            "surname": result.get("surname"),
            "category": result.get("category")
        })
    
    return laureates

def get_country_laureates(client: MongoClient, country: str) -> list[dict]:
    regex = f".*{country}.*"
    results = client["nobel"]["laureates"].find({"bornCountry": {"$regex": regex}}, {"_id": 0, "firstname": 1, "surname": 1, "bornCountry": 1})
    laureates = []
    for result in results:
        laureates.append({
            "firstname": result.get("firstname"),
            "surname": result.get("surname"),
            "bornCountry": result.get("bornCountry")
        })
    return laureates

# Exercice 5 :

def get_shared_prizes(client: MongoClient) -> list[dict]:
    pipeline = [
        {
            "$match": {
                "laureates": {"$exists": True, "$ne": None}, 
                "$expr": {"$gt": [{"$size": "$laureates"}, 1]}
            }
        },
        {
            "$project": {
                "_id": 0,
                "year": 1,
                "category": 1,
                "laureates": 1
            }
        }
    ]
    results = list(client["nobel"]["laureates"].aggregate(pipeline))
    return results

def get_shared_prizes_common(client: MongoClient) -> list[dict]:
    pipeline = [
        {
            "$match": {
                "laureates": {"$exists": True, "$ne": None},
                "$expr": {"$eq": [{"$size": "$laureates"}, 2]}
            }
        },
        {
            "$project": {
                "_id": 0,
                "year": 1,
                "category": 1,
                "laureates": 1,
                "motivation": "$laureates.motivation"
            }
        },
        {
            "$match": {
                "motivation": {
                    "$size": 1
                }
            }
        }
    ]
    results = list(client["nobel"]["laureates"].aggregate(pipeline))
    return results

# Exercice 6 :

def get_laureates_information_sorted(client: MongoClient) -> list[dict]:
    results = client["nobel"]["laureates"].find(
        {},
        {
            "_id": 0,
            "firstname": 1,
            "surname": 1,
            "bornCountry": 1,
            "born": 1
        }
    )
    laureates = list(results)
    sorted_laureates = sorted(
        laureates,
        key=lambda x: (x.get("bornCountry", ""), x.get("born", "")),
        reverse=True
    )
    return sorted_laureates

