## 📊 REST API to MySQL – Football Standings ETL Pipeline

The purpose of this project is to build an ETL (Extract, Transform, Load) pipeline in Python that consumes football standings data from the API-Football (API-Sports) service, processes it, and inserts/updates (UPSERT) the records into a MySQL database.

---
## 📁 Pipeline Structure
<img width="1336" height="499" alt="Pipeline" src="https://github.com/user-attachments/assets/4a10a9bd-69a3-4fca-846d-4b4848ecc76a" />

---

## 🧩 Project Overview

The pipeline is composed of three main stages:

**1. Extract**
  - Connects to the [API-Football REST API](https://www.api-football.com/)
  - Fetches Premier League standings for the chosen season

**2. Transform**
   - Parses JSON response
   - Builds a structured Pandas DataFrame
   - Normalizes and organizes columns

**3. Load**
   - Connects to MySQL using PyMySQL
   - Verifies table existence
   - Performs UPSERT to insert/update standings

---

## 🛠️ Technologies Used
  - Python 3
  - Requests
  - Pandas
  - python-dotenv
  - PyMySQL
  - API-Football (API-Sports)
  - MySQL

---

## 🚀 How to Run This Project
### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY 
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Create a .env file
```text
API_KEY=your_api_sports_key_here
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=football_db
```
### 4. Create the MySQL table
```sql
CREATE TABLE IF NOT EXISTS standings (
	season INT NOT NULL,
    position INT NOT NULL,
    team_id INT NOT NULL,
    team VARCHAR(100) NOT NULL,
    played INT NOT NULL,
    won INT NOT NULL, 
    draw INT NOT NULL,
	lost INT NOT NULL, 
    goals_for INT NOT NULL,
	goals_against INT NOT NULL, 
    goal_diff INT NOT NULL,
	points INT NOT NULL, 
    form VARCHAR(5) NOT NULL,
    PRIMARY KEY (season, team_id),
    UNIQUE KEY uniq_season_position (season, position)
);
```
### 5. Run the ETL script
```bash
python main.py
```
---
## 🔄 UPSERT Logic
The project uses MySQL’s UPSERT pattern:
```sql
INSERT INTO standings (...)
VALUES (...) AS src
ON DUPLICATE KEY UPDATE
    position = src.position,
    team = src.team,
    played = src.played,
    won = src.won,
    draw = src.draw,
    lost = src.lost,
    goals_for = src.goals_for,
    goals_against = src.goals_against,
    goal_diff = src.goal_diff,
    points = src.points,
    form = src.form;
```

This ensures:
 - New data is inserted
 - Existing rows are updated automatically

---
## 📦 Possible Improvements
- Add support for multiple leagues
- Automate the pipeline using cron, Airflow, or Task Scheduler
- Push data to a cloud Data Warehouse
- Build dashboards (Power BI, Grafana, Metabase, Looker)

---
## 🧠 What I've learned with this project
- Extract data from any REST API
- Transform JSON into usable formats
- Leverage Pandas lib for data transformation
- Load data into SQL databases
- Automate the entire process
