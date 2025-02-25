from pymongo import MongoClient
from sqlalchemy import create_engine, text
import datetime

mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["nhl_db"]

engine = create_engine("mysql+mysqlconnector://root:Bmf032502@localhost/nhl_db_new")

def create_tables():
    # sql structure creation tables if they dont exist update if they do
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS games (
                game_id VARCHAR(20) PRIMARY KEY,
                season VARCHAR(10),
                game_date DATE,
                venue VARCHAR(50),
                home_team VARCHAR(10),
                away_team VARCHAR(10),
                home_score INT,
                away_score INT
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS team_stats (
                id INT AUTO_INCREMENT PRIMARY KEY,
                game_id VARCHAR(20),
                team VARCHAR(10),
                shots INT,
                goals INT,
                save_pct FLOAT,
                power_play_pct FLOAT,
                faceoff_pct FLOAT,
                blocked_shots INT,
                hits INT,
                FOREIGN KEY (game_id) REFERENCES games(game_id)
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS player_stats (
                id INT AUTO_INCREMENT PRIMARY KEY,
                game_id VARCHAR(20),
                player_id INT,
                team VARCHAR(10),
                position VARCHAR(5),
                goals INT,
                assists INT,
                sog INT,
                toi VARCHAR(10),
                faceoff_pct FLOAT,
                FOREIGN KEY (game_id) REFERENCES games(game_id)
            )
        """))
        conn.commit()

def insert_game_data(game, conn):
    #pull from mongo and define the data to be inserted into sql
    game_id = game["_id"]
    season = game["boxscoreJSON"]["season"]
    game_date = game["boxscoreJSON"]["gameDate"]
    venue = game["boxscoreJSON"]["venue"]["default"]
    home_team = game["boxscoreJSON"]["homeTeam"]["abbrev"]
    away_team = game["boxscoreJSON"]["awayTeam"]["abbrev"]
    home_score = game["boxscoreJSON"]["homeTeam"]["score"]
    away_score = game["boxscoreJSON"]["awayTeam"]["score"]

    print("game:", game_id, game_date, home_team, "vs", away_team)
    
    #insert values into sql defined earlier. if game already exists update values this is for games only
    sql = text("""
        INSERT INTO games (game_id, season, game_date, venue, home_team, away_team, home_score, away_score)
        VALUES (:game_id, :season, :game_date, :venue, :home_team, :away_team, :home_score, :away_score)
        ON DUPLICATE KEY UPDATE home_score=VALUES(home_score), away_score=VALUES(away_score)
    """)
    conn.execute(sql, {
        "game_id": game_id,
        "season": season,
        "game_date": game_date,
        "venue": venue,
        "home_team": home_team,
        "away_team": away_team,
        "home_score": home_score,
        "away_score": away_score
    })

#same as above but for team stats
def insert_team_stats(game, conn):
    game_id = game["_id"]
    for team_side in ["homeTeam", "awayTeam"]:
        team = game["boxscoreJSON"][team_side]["abbrev"]
        shots = game["boxscoreJSON"][team_side]["sog"]
        goals = game["boxscoreJSON"][team_side]["score"]

        #save percentage is calculated by dividing total saves by total shots against

        goalies = game["boxscoreJSON"]["playerByGameStats"][team_side]["goalies"]
        total_saves = sum(int(g.get("saves", 0)) for g in goalies)
        total_shots_against = sum(int(g.get("shotsAgainst", 0)) for g in goalies)
        if total_shots_against > 0:
            save_pct = round((total_saves / total_shots_against) * 100, 2)
        else:
            save_pct = None

       #calculate blocked shots and hits for each team

        players = game["boxscoreJSON"]["playerByGameStats"][team_side]
        forwards = players.get("forwards", [])
        defense = players.get("defense", [])
        blocked_shots = sum(p.get("blockedShots", 0) for p in forwards + defense)
        hits = sum(p.get("hits", 0) for p in forwards + defense)

        print("team stats for", team)
        sql = text("""
            INSERT INTO team_stats (game_id, team, shots, goals, save_pct, blocked_shots, hits)
            VALUES (:game_id, :team, :shots, :goals, :save_pct, :blocked_shots, :hits)
            ON DUPLICATE KEY UPDATE shots=VALUES(shots), goals=VALUES(goals), save_pct=VALUES(save_pct),
                                    blocked_shots=VALUES(blocked_shots), hits=VALUES(hits)
        """)
        conn.execute(sql, {
            "game_id": game_id,
            "team": team,
            "shots": shots,
            "goals": goals,
            "save_pct": save_pct,
            "blocked_shots": blocked_shots,
            "hits": hits
        })

#same as above but for player stats
def insert_player_stats(game, conn):
    game_id = game["_id"]
    for team_side in ["homeTeam", "awayTeam"]:
        team = game["boxscoreJSON"][team_side]["abbrev"]
        for pos_type in ["forwards", "defense", "goalies"]:
            for player in game["boxscoreJSON"]["playerByGameStats"][team_side].get(pos_type, []):
                player_id = player["playerId"]
                position = player["position"]
                goals = player.get("goals", 0)
                assists = player.get("assists", 0)
                sog = player.get("sog", 0)
                toi = player.get("toi", "00:00")
                faceoff_pct = player.get("faceoffWinningPctg", None)

                print("player", player_id, "for team", team)
                sql = text("""
                    INSERT INTO player_stats (game_id, player_id, team, position, goals, assists, sog, toi, faceoff_pct)
                    VALUES (:game_id, :player_id, :team, :position, :goals, :assists, :sog, :toi, :faceoff_pct)
                    ON DUPLICATE KEY UPDATE goals=VALUES(goals), assists=VALUES(assists), sog=VALUES(sog),
                                            toi=VALUES(toi), faceoff_pct=VALUES(faceoff_pct)
                """)
                conn.execute(sql, {
                    "game_id": game_id,
                    "player_id": player_id,
                    "team": team,
                    "position": position,
                    "goals": goals,
                    "assists": assists,
                    "sog": sog,
                    "toi": toi,
                    "faceoff_pct": faceoff_pct
                })

def migrate_data():
    seasons = ["2019_20_reg", "2020_21_reg", "2021_22_reg", "2022_23_reg", "2023_24_reg"]
    with engine.begin() as conn:
        for season in seasons:
            collection_name = "boxscores_" + season
            collection = mongo_db[collection_name]
            print("\nseason:", season)
            count = 0
            for game in collection.find():
                print("game ID:", game["_id"], "Date:", game["boxscoreJSON"]["gameDate"])
                insert_game_data(game, conn)
                insert_team_stats(game, conn)
                insert_player_stats(game, conn)
                count += 1
                if count % 10 == 0:
                    print(count, "games for", season)
            print(count, "games")

if __name__ == '__main__':
    create_tables()
    migrate_data()
    mongo_client.close()
    print("complete")
