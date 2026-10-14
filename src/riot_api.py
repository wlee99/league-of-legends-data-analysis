import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")

headers = {
    "X-Riot-Token": API_KEY
}

# Helper function to handle rate-limiting error for Riot API requests
def riot_get(url, params=None):
    while True:
        response = requests.get(
            url,
            headers=headers,
            params=params
        )

        if response.status_code == 429:
            wait_time = int(response.headers.get("Retry-After", 1))
            print(f"Rate limited. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            continue

        response.raise_for_status()

        return response.json()

# Gets the PUUID by the Summoner name and tag line
def get_puuid(game_name, tag_line):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    get_summoner_data = riot_get(url)
    return get_summoner_data["puuid"]

# Gets the match ids for the requested PUUID
def get_match_ids(puuid, get_matches_params):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    return riot_get(url, params=get_matches_params)

# Gets the total match data(includes data for all players of a match) for a specific match id
def get_match_data(match_id):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
    return riot_get(url)

# Gets the match data of only the requested PUUID from the total match data
def get_my_match_data(match_data, puuid):
    participants = match_data["info"]["participants"]
    for participant in participants:
        if puuid == participant["puuid"]:
            # Match information
            participant["match_id"] = match_data["metadata"]["matchId"]
            participant["game_creation"] = match_data["info"]["gameCreation"]
            participant["game_duration"] = match_data["info"]["gameDuration"]
            participant["queue_id"] = match_data["info"]["queueId"]

            return participant


