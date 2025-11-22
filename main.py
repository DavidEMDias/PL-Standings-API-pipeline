import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv
import pymysql

# Load the environment variables 
load_dotenv()

API_KEY         = os.getenv("API_KEY")
SEASON          = 2023 #Year the Season Starts
LEAGUE_ID       = 39 #Premier League
MYSQL_HOST      = os.getenv("MYSQL_HOST")
MYSQL_PORT      = os.getenv("MYSQL_PORT")
MYSQL_USER      = os.getenv("MYSQL_USER")
MYSQL_PASSWORD  = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE  = os.getenv("MYSQL_DATABASE")


url         = "https://v3.football.api-sports.io/standings"
headers     = {'x-apisports-key': API_KEY}
querystring = {"league": LEAGUE_ID, "season": SEASON}

#EXTRACT
response = requests.get(url = url, headers=headers, params=querystring)
payload = response.json()



# Extracting the standings information
standings_list = payload["response"][0]["league"]["standings"][0]



# List to hold extracted data
rows = []

# Parsing through each team's standing
for club in standings_list:
    season          = 2023
    position        = club["rank"]
    team_id         = club["team"]["id"]
    team            = club["team"]["name"]
    played          = club["all"]["played"]
    won             = club["all"]["win"]
    draw            = club["all"]["draw"]
    lost            = club["all"]["lose"]
    goals_for       = club["all"]["goals"]["for"]
    goals_against   = club["all"]["goals"]["against"]
    goal_diff       = club["goalsDiff"]
    points          = club["points"]
    form            = club["form"]

    tuple_of_club_records = (season, position, team_id, team, played, won, draw, lost, goals_for, goals_against, goal_diff, points, form)

    rows.append(tuple_of_club_records)


# Create DataFrame
column_names = ['season','position','team_id','team','played', 'won', 'draw', 'lost', 'goals_for', 'goals_against', 'goal_diff', 'points', 'form']
df = pd.DataFrame(rows, columns=column_names)

# Display DataFrame
print(df.to_string(index=False))



# Set up MySQL database connection
db_connection = pymysql.connect(
    host = MYSQL_HOST,
    port = int(MYSQL_PORT),
    user = MYSQL_USER,
    password = MYSQL_PASSWORD,
    connect_timeout = 10,
    autocommit = False,
    database= MYSQL_DATABASE
)

# Get a cursor from the database
cur = db_connection.cursor()
print(f"[SUCCESS] - Connection to database was succesfull!")



# Verify 'standings' table existence in MySQL database
sql_table = "standings"
cur.execute("SHOW TABLES LIKE %s", (f"{sql_table}",) ) 

if cur.fetchone() is None:
    raise SystemExit(f"Table '{sql_table}' was NOT found ... please create it...") #Stop process if it doesn't find results
else:
    print(f"[SUCCESS] - The table '{sql_table}' exists! Continue to the next phase!")




# UPSERT operation
table_cols = ['season','position','team_id','team','played', 'won', 'draw', 'lost', 'goals_for', 'goals_against', 'goal_diff', 'points', 'form']
standings_df = df[table_cols]

# Extract rows as tuples from the dataframe
standings_records_tuples = standings_df.itertuples(index=False, name=None)

# Convert iterator into list of tuples
list_of_standings_records_tuples = list(standings_records_tuples)


# Use SQL to upsert data into the Premier League table 
UPSERT_SQL = f"""
    INSERT INTO {sql_table}
    (season, position, team_id, team, played, won, draw, lost, goals_for, goals_against, goal_diff, points, form)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) as src
    ON DUPLICATE KEY UPDATE
    position        = src.position,
    team            = src.team,
    played          = src.played,
    won             = src.won,
    draw            = src.draw,
    lost            = src.lost,
    goals_for       = src.goals_for,
    goals_against   = src.goals_against,
    goal_diff       = src.goal_diff,
    points          = src.points,
    form            = src.form;
"""


no_of_rows_uploaded_to_mysql = len(list_of_standings_records_tuples)


# LOAD
try:
    cur.executemany(UPSERT_SQL, list_of_standings_records_tuples)
    db_connection.commit()
    print(f"[SUCCESS] - Upsert attempted for {no_of_rows_uploaded_to_mysql} rows!")
except Exception as e:
    db_connection.rollback()
    print(f"[ERROR] - Rolled back due to this: {e}")
finally:
    cur.close() #close cursor
    db_connection.close() #close connection
    print("All database connections now closed. \n\nClean up completed.")