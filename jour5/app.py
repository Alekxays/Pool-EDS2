from fastapi import FastAPI, HTTPException, Query, Depends
from pymongo import MongoClient
from bson.objectid import ObjectId
from collections import defaultdict
from datetime import datetime
import logging

app = FastAPI()

client = MongoClient("localhost", 27017)

# Partie 2 :

@app.get("/")
def hello():
    return {"message": "Hello world, this is my first web API!"}

@app.get("/laureates")
def get_laureates(
    categories: list[str] = Query(None),
    awarded_year: int = Query(None),
):
    try:
        query = {}
        if categories and awarded_year:
            query["prizes"] = {
                "$elemMatch": {
                    "category": {"$in": [c.lower() for c in categories]},
                    "year": str(awarded_year)
                }
            }
        elif categories:
            query["prizes"] = {
                "$elemMatch": {
                    "category": {"$in": [c.lower() for c in categories]}
                }
            }
        elif awarded_year:
            query["prizes"] = {
                "$elemMatch": {
                    "year": str(awarded_year)
                }
            }
        laureates_cursor = client["nobel"]["laureates"].find(query)
        laureates_list = []
        for laureate in laureates_cursor:
            laureate['_id'] = {'$oid': str(laureate['_id'])}
            laureates_list.append(laureate)
        def get_sort_key(laureate):
            earliest_year = min(int(prize['year']) for prize in laureate['prizes'])
            surname = laureate.get('surname', '').lower()
            return (earliest_year, surname)
        laureates_list.sort(key=get_sort_key)
        return laureates_list
    except Exception as e:
        logging.error(f"Error fetching laureates: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching laureates.")

@app.get("/prizes")
def get_prizes(
    before: int = Query(None),
    after: int = Query(None),
    awarded: int = Query(None),
):
    try:
        query = {}
        if awarded is not None:
            if awarded == 1:
                query["laureates"] = {"$exists": True, "$ne": []}
            elif awarded == 0:
                query["laureates"] = {"$exists": False}
        if before is not None:
            query.setdefault("year", {})
            query["year"]["$lte"] = str(before)
        if after is not None:
            query.setdefault("year", {})
            query["year"]["$gte"] = str(after)
        prizes_cursor = client["nobel"]["prizes"].find(query).sort([
            ("year", 1),
            ("category", -1)
        ])
        prizes_list = []
        for prize in prizes_cursor:
            prize['_id'] = {'$oid': str(prize['_id'])}
            prizes_list.append(prize)
        return prizes_list
    except Exception as e:
        logging.error(f"Error fetching prizes: {e}")
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
            category: {
                "total_prizes": total_prizes[category],
                "average_laureates": round(laureates_count[category] / total_prizes[category], 2)
            }
            for category in total_prizes
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
            category: {
                "total_laureates": total_laureates[category],
                "average_age": round(sum(total_age[category]) / len(total_age[category]), 2) if total_age[category] else None,
                "years": sorted(list(prize_years[category]))
            }
            for category in total_laureates
        }
        return statistics
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching laureate statistics.")