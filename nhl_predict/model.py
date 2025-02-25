import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score

path = "G:/NHL Prediction/used tables/"
games = pd.read_csv(path + "games.csv")            
player_stats = pd.read_csv(path + "player_stats.csv")  
goalie_stats = pd.read_csv(path + "goalie_stats.csv")  
final_rosters = pd.read_csv(path + "final_rosters_2024.csv")  
future_schedule = pd.read_csv(path + "nhl-202324-asplayed.csv")    
old_seasons = games[games["season"] < 20232024].copy()

final_skater = pd.merge(player_stats, final_rosters, on="player_id", suffixes=("", "_final"))
final_skater["games_played"] = 1

#sum of all historic skater stats
player_tot = final_skater.groupby("player_id", as_index=False).agg({
    "goals": "sum",
    "assists": "sum",
    "sog": "sum",
    "toi_seconds": "sum",  #unused
    "games_played": "sum"
})

player_tot["goals_per_game"] = (player_tot["goals"] / player_tot["games_played"]).round().astype(int)
player_tot["assists_per_game"] = (player_tot["assists"] / player_tot["games_played"]).round().astype(int)
player_tot["sog_per_game"] = (player_tot["sog"] / player_tot["games_played"]).round().astype(int)

player_avg = pd.merge(player_tot, final_rosters, on="player_id")

#apply player stats to team stats
team_avg = player_avg.groupby("team", as_index=False).agg({
    "goals_per_game": "sum",
    "assists_per_game": "sum",
    "sog_per_game": "sum"
})
team_avg.rename(columns={
    "goals_per_game": "final_goals_pg",
    "assists_per_game": "final_assists_pg",
    "sog_per_game": "final_sog_pg"
}, inplace=True)

#goalie save pct summed
final_goalie = pd.merge(goalie_stats, final_rosters, on="player_id", suffixes=("", "_final"))
final_goalie["team"] = final_goalie["team"]

# avg of goalie save pct
goalie_avg = final_goalie.groupby("player_id", as_index=False).agg({
    "save_pct": "mean"
})
goalie_avg = pd.merge(goalie_avg, final_rosters, on="player_id")
#calculate mean of goalie save pct
goalie_tot = goalie_avg.groupby("team", as_index=False).agg({
    "save_pct": "mean"
})
goalie_tot.rename(columns={"save_pct": "final_goalie_save_pct"}, inplace=True)

# goalie and player stats become team stats as an aveage
team_tot = pd.merge(team_avg, goalie_tot, on="team", how="outer")
print("\n team stats done")

#team stats go into training data linking to the correct teams
games_home_tot = pd.merge(old_seasons, team_tot, left_on="home_team", right_on="team", how="left")
games_home_tot.rename(columns={
    "final_goals_pg": "home_goals_pg",
    "final_assists_pg": "home_assists_pg",
    "final_sog_pg": "home_sog_pg",
    "final_goalie_save_pct": "home_goalie_save_pct"
}, inplace=True)
games_home_tot.drop(columns=["team"], inplace=True)

games_away_tot = pd.merge(games_home_tot, team_tot, left_on="away_team", right_on="team", how="left")
games_away_tot.rename(columns={
    "final_goals_pg": "away_goals_pg",
    "final_assists_pg": "away_assists_pg",
    "final_sog_pg": "away_sog_pg",
    "final_goalie_save_pct": "away_goalie_save_pct"
}, inplace=True)
games_away_tot.drop(columns=["team"], inplace=True)

df_to_model = games_away_tot.copy()

# win definition if 0 home wins, if 1 away wins
df_to_model["label"] = np.where(df_to_model["home_score"] > df_to_model["away_score"], 0, 1)

# Define feature set.
game_features = [
    "home_goals_pg", "home_assists_pg", "home_sog_pg", "home_goalie_save_pct",
    "away_goals_pg", "away_assists_pg", "away_sog_pg", "away_goalie_save_pct"
]
df_to_model.dropna(subset=game_features + ["label"], inplace=True)

x_train = df_to_model[game_features]
y_train = df_to_model["label"]

#training with xgboost 80/20 split
x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=42)

model_builder = xgb.XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    objective="binary:logistic",
    use_label_encoder=False
)
model_builder.fit(x_train, y_train)

y_testing = model_builder.predict(x_test)
accuracy_testing = accuracy_score(y_test, y_testing)
print(f"\naccuracy {accuracy_testing:.3f}") # not sure if this is working

#prediction calculations. calls from earlier team sums and avgs based on player data and links it into the future schedule
final_pred_home = pd.merge(future_schedule, team_tot, left_on="home_team", right_on="team", how="left")
final_pred_home.rename(columns={
    "final_goals_pg": "home_goals_pg",
    "final_assists_pg": "home_assists_pg",
    "final_sog_pg": "home_sog_pg",
    "final_goalie_save_pct": "home_goalie_save_pct"
}, inplace=True)
final_pred_home.drop(columns=["team"], inplace=True)

final_pred_away = pd.merge(final_pred_home, team_tot, left_on="away_team", right_on="team", how="left")
final_pred_away.rename(columns={
    "final_goals_pg": "away_goals_pg",
    "final_assists_pg": "away_assists_pg",
    "final_sog_pg": "away_sog_pg",
    "final_goalie_save_pct": "away_goalie_save_pct"
}, inplace=True)
final_pred_away.drop(columns=["team"], inplace=True)

df_final = final_pred_away.copy()
df_final.dropna(subset=game_features, inplace=True)

x_pred = df_final[game_features]
pred_final = model_builder.predict(x_pred)
df_final["predicted_winner"] = np.where(pred_final == 0, "Home", "Away")

# columns to be saved in prediction
output_cols = ["game_id", "game_date", "home_team", "away_team"] + game_features + ["predicted_winner"]
output_cols = [col for col in output_cols if col in df_final.columns]

out_file = path + "predicted_future_schedule_e.csv"
df_final[output_cols].to_csv(out_file, index=False)
print(f"complete")