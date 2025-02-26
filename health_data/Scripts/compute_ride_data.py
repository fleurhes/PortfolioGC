from sqlalchemy import create_engine
import pandas as pd

user = "root"
password = "Bmf032502"
host = "localhost"
db_name = "health_data"
csv_path = "C:/Users/bflor/OneDrive/Documents/github/health_data/cycling_data.csv"

conn_str = f"mysql+mysqlconnector://{user}:{password}@{host}/{db_name}"
engine = create_engine(conn_str)

def populate_intensity_and_time_since_ride():
    query = "SELECT id, date_time, distance, heart_rate_max, elevation_gain FROM cycling_data"
    data = pd.read_sql(query, engine)

    data["date_time"] = pd.to_datetime(data["date_time"])
    data = data.sort_values("date_time")

    data["ride_intensity"] = (data["heart_rate_max"] + data["distance"] * 10 + data["elevation_gain"] / 10) / 3

    time_diffs = []
    prev_time = None
    for current in data["date_time"]:
        if prev_time is None:
            time_diffs.append(0)
        else:
            diff_hours = (current - prev_time).total_seconds() / 3600.0
            time_diffs.append(diff_hours)
        prev_time = current
    data["hours_since_last_ride"] = time_diffs

    with engine.begin() as conn:
        for _, row in data.iterrows():
            update = "UPDATE cycling_data SET ride_intensity = %f, hours_since_last_ride = %f WHERE id = %d" % (
                row["ride_intensity"], row["hours_since_last_ride"], row["id"]
            )
            conn.exec_driver_sql(update)
    
    print("complete")

if __name__ == '__main__':
    populate_intensity_and_time_since_ride()
