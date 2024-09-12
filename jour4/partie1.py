from pymongo import MongoClient

# Exercice 1 :

def get_mongo_client(host:str, port:int) -> MongoClient:
    return MongoClient(host, port)

# Exercice 2 :

def get_all_laureates(client:MongoClient) -> list:
    return list(client["nobel"]["laureates"].find())

# Exercice 3 :

def get_laureates_information(client: MongoClient) -> list[dict]:
    return list(client["nobel"]["laureates"].find({}, {"_id": 0, "firstname": 1, "surname": 1, "born": 1}))

def get_prize_categories(client: MongoClient) -> list[str]:
    return list(client["nobel"]["prizes"].distinct("category"))

# Exercice 4 :

def get_category_laureates(client: MongoClient, category: str) -> list[dict]:
    results = client["nobel"]["laureates"].find(
        {"prizes.category": category},
        {"_id": 0, "firstname": 1, "surname": 1, "prizes.category": 1}
    )
    laureates = []
    for result in results:
        prizes = [{"category": prize.get("category")} for prize in result.get("prizes", [])]
        laureates.append({
            "firstname": result.get("firstname"),
            "surname": result.get("surname"),
            "prizes": prizes
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
                "laureates": {"$exists": True, "$ne": []},
                "$expr": {"$gt": [{"$size": "$laureates"}, 1]}
            }
        },
        {
            "$project": {
                "year": 1,
                "category": 1,
                "laureates": 1
            }
        }
    ]
    results = list(client["nobel"]["prizes"].aggregate(pipeline))
    return results


def get_shared_prizes_common(client: MongoClient) -> list[dict]:
    pipeline = [
        {
            "$match": {
                "$expr": {"$eq": [{"$size": "$laureates"}, 2]}
            }
        },
        {
            "$project": {
                "year": 1,
                "category": 1,
                "laureates": 1,
                "motivation_list": {
                    "$map": {
                        "input": "$laureates",
                        "as": "laureate",
                        "in": "$$laureate.motivation"
                    }
                }
            }
        },
        {
            "$addFields": {
                "unique_motivations": {
                    "$size": {
                        "$setUnion": ["$motivation_list"]
                    }
                }
            }
        },
        {
            "$match": {
                "unique_motivations": 1
            }
        }
    ]
    results = list(client["nobel"]["prizes"].aggregate(pipeline))
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
    def clean_country(country: str) -> str:
        country = country.lower()
        if country.startswith('the '):
            return country[4:]
        return country
    sorted_laureates = sorted(
        laureates,
        key=lambda x: (
            clean_country(x.get("bornCountry", "")),
            x.get("born", "")
        )
    )
    return sorted_laureates
