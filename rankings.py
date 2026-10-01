import sqlite3
import requests
import pandas as pd

conn = sqlite3.connect("basketball.db")
cursor = conn.cursor()

cursor.execute("""
  SELECT 
    game_id,
    team_id,
    points,
    field_goals_attempted,
    offensive_rebounds,
    total_rebounds,
    turnovers,
    personal_fouls,
    field_goal_attempts_allowed,
    offensive_rebounds_allowed,
    total_rebounds_allowed,
    turnovers_forced,
    fouls_drawn,
    ppp,
    papp
  FROM team_game_stats
""")

games = pd.DataFrame(cursor.fetchall(), columns=[
  "game_id",
  "team_id",
  "points",
  "feild_goals_attempted",
  "offensive_rebounds",
  "total_renounds",
  "turnovers",
  "personal_fouls",
  "feild_goal_attempts_allowed",
  "offensive_rebound_allowed",
  "total_rebounds_allowed",
  "turnovers_forced",
  "fouls_drawn",
  "ppp",
  "papp"
])
opp_data = games.merge(
  games,
  on="game_id",
  suffixes=("", "_opp")
)

opp_data = opp_data[
  opp_data["team_id"] != opp_data["team_id_opp"]
]

opp_avg_ppp = opp_data.groupby("team_id")["ppp_opp"].mean()

opp_avg_papp = opp_data.groupby("team_id")["papp_opp"].mean()

team_data = games.groupby(["team_id"]).agg(
  ppp = ("ppp", "mean"),
  papp = ("papp", "mean"),
  games = ("game_id", "count")
)

team_data["opp_avg_ppp"] = opp_avg_ppp
team_data["opp_avg_papp"] = opp_avg_papp

team_data["off_adj"] = (
  (team_data["ppp"] / team_data["opp_avg_papp"])
)

team_data["def_adj"] = (
  (team_data["papp"] / team_data["opp_avg_ppp"])
) 

games = games.merge(
  team_data[["off_adj","def_adj"]],
  left_on = "game_id",
  right_index=True
)

opp_data = games.merge(
  games,
  on = "game_id",
  suffixes = ("","_opp")
)

opp_data = opp_data[
  opp_data["team_id"] != opp_data["team_id_opp"]
]

opp_avg_def = opp_data.groupby("team_id")["def_adj_opp"].mean()
opp_avg_off = opp_data.groupby("team_id")["off_adj_opp"].mean()

team_data["opp_avg_def"] = opp_avg_def
team_data["opp_avg_off"] = opp_avg_off

team_data["adj_ppp"] = (
  team_data["ppp"] / team_data["opp_avg_def"]
)

team_data["adj_papp"] = (
  team_data["papp"] / team_data["opp_avg_off"]
)

games = games.merge(
  team_data[["adj_ppp","adj_papp"]],
  left_on = "game_id",
  right_index=True
)

opp_data = games.merge(
  games,
  on = "game_id",
  suffixes = ("","_opp")
)

opp_data = opp_data[
  opp_data["team_id"] != opp_data["team_id_opp"]
]

opp_avg_adj_papp = opp_data.groupby("team_id")["adj_papp_opp"].mean()
opp_avg_adj_ppp = opp_data.groupby("team_id")["adj_ppp_opp"].mean()

team_data["opp_avg_adj_papp"] = opp_avg_adj_papp
team_data["opp_avg_adj_ppp"] = opp_avg_adj_ppp

team_data["sos_ppp"] = (
  team_data["ppp"] / team_data["opp_avg_adj_papp"]
)

team_data["sos_papp"] = (
  team_data["papp"] / team_data["opp_avg_adj_ppp"]
)

print(team_data[["ppp", "papp", "off_adj", "def_adj", "sos_ppp", "sos_papp"]].head(20))

print("Top Ten Offenses:")
print(team_data.nlargest(10, "sos_ppp")[["sos_ppp"]])

print("Bottoms Ten Offenses")
print(team_data.nsmallest(10, "sos_ppp")[["sos_ppp"]])

print("Bottom Ten Defenses:")
print(team_data.nlargest(10, "sos_papp")[["sos_papp"]])

print("Top Ten Defenses")
print(team_data.nsmallest(10, "sos_papp")[["sos_papp"]])


  
  
  
