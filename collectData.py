import requests
import json
from pathlib import Path
from time import sleep
import random


api_key = "RGAPI-54a6da2f-fa03-49c6-a37e-dfb37ec9a5bc"

def get_puuid(summoner_name):
    api_url = (
        "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" +
        summoner_name +
        "?api_key=" +
        api_key
    )  
    resp = requests.get(api_url)
    player_info = resp.json()
    puuid = player_info['puuid']
    return puuid  

def get_match_ids(puuid):
    api_url = (
        "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/" +
        puuid + 
        "/ids?start=0&count=20" + 
        "&api_key=" + 
        api_key
    ) 
    resp = requests.get(api_url)
    match_ids = resp.json()
    return match_ids

def get_match_data(match_id):
    api_url = (
        "https://europe.api.riotgames.com/lol/match/v5/matches/" +
        match_id + 
        "?api_key=" + 
        api_key
    )
    
    resp = requests.get(api_url)
    match_data = resp.json()
    return match_data

def check_for_limit(api_call):
    if api_call == 100:
        print("Sleeping")
        sleep(120)
        return 1
    else:
        return api_call + 1




starting_summoner = input('Pocetni Summoner:')
base = Path('podaci_treniranje')

games_collected = 0
api_call = 0

games_collected_list = []
puuid_checked_list = []

puuid = get_puuid(starting_summoner)
api_call = check_for_limit(api_call)
match_ids = get_match_ids(puuid)
api_call = check_for_limit(api_call)

puuid_checked_list.append(puuid)

while games_collected <= 11000:
    api_call = check_for_limit(api_call)
    match = get_match_data(match_ids[random.randint(0,9)])
    
    for player in match['metadata']['participants']:
        if puuid != player and player not in puuid_checked_list:
            puuid = player
            print(puuid)
            puuid_checked_list.append(puuid)
            break
    api_call = check_for_limit(api_call)
    match_ids = get_match_ids(puuid)

    for game in match_ids:
        jsonpath = base / (str(games_collected) + ".json")

        api_call = check_for_limit(api_call)
        data = get_match_data(game)
        if data['metadata']['matchId'] not in games_collected_list:
            print(data['metadata']['matchId'])
            jsonpath.write_text(json.dumps(data))
            games_collected = games_collected + 1
            games_collected_list.append(data['metadata']['matchId'])
print("Done")


