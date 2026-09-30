import sqlite3
import requests

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
    ppp,
    papp
  FROM teamBocscore
""")

games = cursor.fetchall()



  
  
  
