import os
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:Bmf032502@localhost/nhl_db")

save_folder = r"G:\NHL Prediction\database tables"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

tables = [
    "games",
    "player_stats",
    "team_stats"
]

with engine.connect() as connection:
    for table in tables:
        query = "SELECT * FROM " + table
        df = pd.read_sql(query, connection)
        csv_path = os.path.join(save_folder, table + ".csv")
        df.to_csv(csv_path, index=False)
        print("exported " + table)

print("complete")
