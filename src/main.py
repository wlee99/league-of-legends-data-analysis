import json
import os
from dotenv import load_dotenv
from riot_api import *
from database import *

load_dotenv()

game_name = os.getenv("GAME_NAME")
tag_line = os.getenv("TAG_LINE")

puuid = get_puuid(game_name, tag_line)

match_ids = []

for start in range(0, 200, 100):
    params = {
        "start": start,
        "count": 100
    }

    new_match_ids = get_match_ids(puuid, params)
    match_ids.extend(new_match_ids)

match_data_list = []
for match_id in match_ids:
    match_data = get_match_data(match_id)
    match_data_list.append(match_data)

my_match_data_list = []
for match_data in match_data_list:
    participant = get_my_match_data(match_data, puuid)
    my_match_data_list.append(participant)

with open("matches.json", "w") as file:
    json.dump(my_match_data_list, file, indent=4)

conn = connect_db()

for match in my_match_data_list:
    insert_match(conn, match)

conn.close()

