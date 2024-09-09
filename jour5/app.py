from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from bson.json_util import dumps
from collections import defaultdict
from datetime import datetime

app = FastAPI()

# Partie 2 :

@app.get("/")
def hello():
    return {"message": "Hello world, this is my first web API!"}

client = MongoClient("localhost", 27017)

@app.get("/laureates")
def laureates(categories: list[str] = Query(None), awarded_year: int = Query(None)):
    try:
        query = {}
        if categories:
            query["prizes.category"] = {"$in": categories}
        if awarded_year:
            query["prizes.year"] = awarded_year
        laureates_cursor = client["nobel"]["laureates"].find(query).sort([
            ("prizes.year", 1),
            ("surname", 1)
        ])
        laureates_json = dumps(laureates_cursor)
        return {"laureates": laureates_json}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching laureates.")

@app.get("/prizes")
def prizes(before: int = Query(None), after: int = Query(None), awarded: int = Query(None)):
    try:
        query = {}
        if awarded is not None:
            if awarded == 1:
                query["laureates"] = {"$exists": True, "$ne": []}
            elif awarded == 0:
                query["laureates"] = {"$exists": False}
        if before:
            query["year"] = {"$lte": before}
        if after:
            query["year"] = {"$gte": after}
        prizes_cursor = client["nobel"]["prizes"].find(query).sort([
            ("year", 1),
            ("category", -1)
        ])
        prizes_json = dumps(prizes_cursor)
        return {"prizes": prizes_json}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching Nobel prizes.")

# Partie 3 :

@app.get("/prizes_statistics")
def prizes_statistics(
    start: int = Query(None), 
    end: int = Query(None), 
    categories: list[str] = Query(None)
):
    try:
        query = {}
        if start:
            query["year"] = {"$gte": start}
        if end:
            if "year" in query:
                query["year"]["$lte"] = end
            else:
                query["year"] = {"$lte": end}
        if categories:
            query["category"] = {"$in": categories}
        prizes_cursor = client["nobel"]["prizes"].find(query)
        total_prizes = defaultdict(int)
        laureates_count = defaultdict(int)
        for prize in prizes_cursor:
            category = prize["category"]
            total_prizes[category] += 1
            laureates_count[category] += len(prize.get("laureates", []))
        statistics = {
            "total_prizes": {category: total for category, total in total_prizes.items()},
            "average_laureates_per_prize": {
                category: round(laureates_count[category] / total_prizes[category], 2) 
                if total_prizes[category] > 0 else 0 
                for category in total_prizes
            }
        }
        return statistics
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching prize statistics.")
    
@app.get("/laureates_statistics")
def laureates_statistics(
    gender: str = Query(None), 
    country_code: str = Query(None), 
    categories: list[str] = Query(None)
):
    try:
        query = {}
        if gender:
            query["gender"] = gender
        if country_code:
            query["bornCountryCode"] = country_code
        if categories:
            query["prizes.category"] = {"$in": categories}
        laureates_cursor = client["nobel"]["laureates"].find(query)
        total_laureates = defaultdict(int)
        total_age = defaultdict(list)
        prize_years = defaultdict(set)
        for laureate in laureates_cursor:
            for prize in laureate.get("prizes", []):
                category = prize["category"]
                year = int(prize["year"])
                total_laureates[category] += 1
                prize_years[category].add(year)
                birth_date_str = laureate.get("born")
                if birth_date_str and birth_date_str != "0000-00-00":
                    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
                    age_at_award = year - birth_date.year
                    total_age[category].append(age_at_award)
        statistics = {
            "total_laureates": {category: total for category, total in total_laureates.items()},
            "average_age_at_award": {
                category: round(sum(ages) / len(ages), 2) 
                if ages else None
                for category, ages in total_age.items()
            },
            "prize_years": {category: sorted(list(years)) for category, years in prize_years.items()}
        }
        return statistics
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching laureate statistics.")