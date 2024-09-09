from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from bson.json_util import dumps
app = FastAPI()

# Exercice 1 :

@app.get("/")
def hello():
    return {"message": "Hello world, this is my first web API!"}

# Exercice 2 :

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

# Exercice 2(bis) :

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
