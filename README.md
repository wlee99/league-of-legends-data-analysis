# League of Legends Match Analysis

A data analytics project that collects my League of Legends match history from the Riot Games API, stores the data in a PostgreSQL, analyzes it with SQL and visualizes the results with PowerBI.

# Tech Stack

- Python
- Riot Games API
- PostgreSQL
- SQL
- PowerBI

# Database

Database name: 'lol_project'

Connect to PostgreSQL: /opt/homebrew/opt/postgresql@18/bin/psql lol_project

Run the SQL command to build the SQL view: /opt/homebrew/opt/postgresql@18/bin/psql lol_project -f analysis.sql

Command to download CSV: \copy (SELECT * FROM match_analysis) TO '/Users/won/Desktop/LoL Data Project/match_analysis.csv' CSV HEADER;

If the SQL return is too long, q and \pset pager off