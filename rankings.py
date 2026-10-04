import sqlite3
import requests
import pandas as pd

conn = sqlite3.connect("basketball.db")
cursor = conn.cursor()

cursor.execute("""
  SELECT 
    tgs.game_id,
    tgs.team_id,
    tgs.points,
    tgs.field_goals_attempted,
    tgs.offensive_rebounds,
    tgs.total_rebounds,
    tgs.turnovers,
    tgs.personal_fouls,
    tgs.field_goal_attempts_allowed,
    tgs.offensive_rebounds_allowed,
    tgs.total_rebounds_allowed,
    tgs.turnovers_forced,
    tgs.fouls_drawn,
    tgs.ppp,
    tgs.papp,
    t.team_name
  FROM team_game_stats tgs
  JOIN teams t
    ON tgs.team_id = t.team_id
""")

games = pd.DataFrame(cursor.fetchall(), columns=[
  "game_id",
  "team_id",
  "points",
  "field_goals_attempted",
  "offensive_rebounds",
  "total_rebounds",
  "turnovers",
  "personal_fouls",
  "field_goal_attempts_allowed",
  "offensive_rebounds_allowed",
  "total_rebounds_allowed",
  "turnovers_forced",
  "fouls_drawn",
  "ppp",
  "papp",
  "team_name"
])
team_data = games.groupby(["team_id"]).agg(
  ppp = ("ppp", "mean"),
  papp = ("papp", "mean"),
  games = ("game_id", "count")
).reset_index()

team_data = team_data.merge(
  games[["team_id", "team_name"]].drop_duplicates(),
  on="team_id",
  how="left"
)
matchups = games[["game_id", "team_id"]].merge(
    games[["game_id", "team_id"]],
    on="game_id",
    suffixes=("", "_opp")
)

matchups = matchups[
    matchups["team_id"] != matchups["team_id_opp"]
]

matchups = matchups.merge(
    team_data[["team_id", "ppp", "papp"]].rename(columns={
        "team_id": "team_id_opp",
        "ppp": "ppp_opp_season",
        "papp": "papp_opp_season"
    }),
    on="team_id_opp",
    how="left"
)

opp_avg_ppp = matchups.groupby("team_id")["ppp_opp_season"].mean()
opp_avg_papp = matchups.groupby("team_id")["papp_opp_season"].mean()

team_data = team_data.merge(
    opp_avg_ppp.rename("opp_avg_ppp"),
    on="team_id",
    how="left"
)

team_data = team_data.merge(
    opp_avg_papp.rename("opp_avg_papp"),
    on="team_id",
    how="left"
)

team_data["off_adj"] = (
    team_data["ppp"] / team_data["opp_avg_papp"]
)

team_data["def_adj"] = (
    team_data["papp"] / team_data["opp_avg_ppp"]
)

matchups = matchups.merge(
    team_data[["team_id","off_adj", "def_adj"]].rename(columns={
        "team_id": "team_id_opp",
        "off_adj": "off_adj_opp",
        "def_adj": "def_adj_opp"
    }),
    on="team_id_opp",
    how="left"

)

opp_avg_adj_def = matchups.groupby("team_id")["def_adj_opp"].mean()
opp_avg_adj_off = matchups.groupby("team_id")["off_adj_opp"].mean()

team_data = team_data.merge(
    opp_avg_adj_def.rename("opp_avg_adj_def"),
    on="team_id",
    how="left"
)

team_data = team_data.merge(
    opp_avg_adj_off.rename("opp_avg_adj_off"),
    on="team_id",
    how="left"
)
team_data["adj_ppp"] = (
    team_data["ppp"] / team_data["opp_avg_adj_def"]
)

team_data["adj_papp"] = (
    team_data["papp"] / team_data["opp_avg_adj_off"]
)

team_data["sos_ppp"] = (
    team_data["ppp"] / team_data["opp_avg_adj_def"]
)

team_data["sos_papp"] = (
    team_data["papp"] / team_data["opp_avg_adj_off"]
)

#print(team_data[["ppp", "papp", "off_adj", "def_adj", "sos_ppp", "sos_papp"]].head(20))

print("Top Ten Offenses:")
print(team_data.nlargest(20, "sos_ppp")[["team_name", "sos_ppp"]])

print("Bottoms Ten Offenses")
print(team_data.nsmallest(20, "sos_ppp")[["team_name", "sos_ppp"]])

print("Bottom Ten Defenses:")
print(team_data.nlargest(20, "sos_papp")[["team_name", "sos_papp"]])

print("Top Ten Defenses")
print(team_data.nsmallest(20, "sos_papp")[["team_name", "sos_papp"]])
