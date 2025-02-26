import requests
import json
from datetime import date, timedelta
from pymongo import MongoClient

def get_sched(date_str):

    url = f"https://api-web.nhle.com/v1/schedule/{date_str}"
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"couldnt get sched {date_str}: HTTP {resp.status_code}")
        return None

def get_score(game_id):

    url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/boxscore"
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"game {game_id} not scored: HTTP {resp.status_code}")
        return None

def days_wanted(start_date, end_date):

    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def store_sched_score(date_str, schedules_coll, boxscores_coll):

    schedule_data = get_sched(date_str)
    if not schedule_data:
        return  

    schedules_coll.update_one(
        {"_id": date_str},  
        {"$set": {"date": date_str, "scheduleJSON": schedule_data}},
        upsert=True
    )

    game_weeks = schedule_data.get("gameWeek", [])
    for gw in game_weeks:
        for game in gw.get("games", []):
            game_id = game.get("id")
            if not game_id:
                continue 

            boxscore_data = get_score(game_id)
            if not boxscore_data:
                continue

            boxscores_coll.update_one(
                {"_id": game_id},
                {"$set": {"game_id": game_id, "date": date_str, "boxscoreJSON": boxscore_data}},
                upsert=True
            )

def main():

    client = MongoClient("mongodb://localhost:27017/")
    db = client["nhl_db"]  

    season_ranges = {
        "2019_20": (date(2019, 10, 2), date(2020, 3, 11)),  
        "2023_24":(date(2023, 10, 10), date(2024, 4, 18))
    }

    for season, (start_date, end_date) in season_ranges.items():

        schedules_collection = db[f"schedules_{season}_reg"]
        boxscores_collection = db[f"boxscores_{season}_reg"]

        for single_date in days_wanted(start_date, end_date):
            date_str = single_date.strftime("%Y-%m-%d")
            store_sched_score(date_str, schedules_collection, boxscores_collection)

    print("\n stored schedules and scores")
    client.close()

if __name__ == "__main__":
    main()
