from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

user = "root"
password = "Bmf032502"
host = "localhost"
db_name = "health_data"
csv_path = "C:/Users/bflor/OneDrive/Documents/github/health_data/cycling_data.csv"

conn_str = f"mysql+mysqlconnector://{user}:{password}@{host}/{db_name}"
engine = create_engine(conn_str)

def run_query(query): #master function to run queries
    df = pd.read_sql_query(query, engine)
    return df

def store_new_tables(df, table_name): #master function to store new tables
    df.to_sql(table_name, engine, if_exists='replace', index=False)

def time(): #find the time of day that is best for cycling
    sql = "SELECT HOUR(date_time) AS ride_hour, AVG(avg_speed) AS avg_speed FROM cycling_data GROUP BY ride_hour ORDER BY avg_speed DESC"
    df = run_query(sql)
    store_new_tables(df, "best_time")
    
    print("time complete.")

def recovery(): #find the recovery time between rides
    sql = "SELECT hours_since_last_ride, AVG(avg_speed) AS avg_speed FROM cycling_data GROUP BY hours_since_last_ride ORDER BY hours_since_last_ride"
    df = run_query(sql)
    store_new_tables(df, "recovery")
    
    print("recovery complete")

def intensity(): #find most intense rides
    sql = "SELECT date_time, distance, ride_intensity FROM cycling_data ORDER BY ride_intensity DESC LIMIT 10"
    df = run_query(sql)
    store_new_tables(df, "intense")

    df['date_time_str'] = df['date_time'].astype(str)

    print("intensity complete.")

def duration():# find longest rides and average speed
    sql = "SELECT duration, AVG(avg_speed) AS avg_speed FROM cycling_data GROUP BY duration ORDER BY duration"
    df = run_query(sql)
    store_new_tables(df, "duration")
    
    print("complete duration.")

def main():
    time()
    recovery()
    intensity()
    duration()
    print("all complete")

if __name__ == '__main__':
    main()
