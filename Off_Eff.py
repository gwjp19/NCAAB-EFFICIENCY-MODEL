import sqlite3

conn = splite3.connect("basketball.db")\cursor = conn.cursor()

cursor.execute("""
  SELECT 
    game_id,
    team_id,
    points,
    feild_goals_attempted,
    offensive_rebounds,
    total_renounds,
    turnovers,
    personal_fouls,
    feild_goal_attempts_allowed,
    offensive_rebound_allowed,
    total_rebounds_allowed,
    turnovers_forced,
    fouls_drawn,
  FROM teamBocscore
""")

games = cursor.fetchall()
  
for game in game_id:
  
