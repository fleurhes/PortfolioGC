from sqlalchemy import create_engine, text
import pandas as pd

user = "root"
password = "Bmf032502"
host = "localhost"
db_name = "health_data"
csv_path = "C:/Users/bflor/OneDrive/Documents/github/health_data/cycling_data.csv"

def make_db():
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}")
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))

def setup_table():
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{db_name}")
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS cycling_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date_time DATETIME,
                duration FLOAT,
                distance FLOAT,
                calories_burned FLOAT,
                heart_rate_max INT,
                heart_rate_avg INT,
                elevation_gain FLOAT,
                avg_speed FLOAT,
                ride_intensity FLOAT,
                hours_since_last_ride FLOAT
            )
        """))

def dump_data():
    df = pd.read_csv(csv_path)
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{db_name}")
    df.to_sql("cycling_data", con=engine, if_exists="append", index=False)

if __name__ == "__main__":
    print("checking if db exists")
    make_db()
    
    print("table setup")
    setup_table()
    
    print("importing from csv")
    dump_data()
    
    print("complete")
