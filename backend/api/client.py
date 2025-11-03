import requests
from models import Player, Match


def get_api_request(url):
    response  = requests.get(url)
    data = response.json()
    return data

def get_player_data(account_id):
    url = f"https://api.opendota.com/api/players/{account_id}"
    win_lose_url = f"https://api.opendota.com/api/players/{account_id}/wl"

    player_data = get_api_request(url)
    win_lose_data = get_api_request(win_lose_url)
    profile = player_data.get('profile')

    rank_tier = player_data.get("rank_tier")

    if not player_data:
        return None
    
    if rank_tier == None:
        rank_tier = 0

    player = Player(
        account_id= account_id,
        personaname= profile.get("personaname"),
        avatar_url= profile.get("avatarfull"),
        rank_tier= rank_tier,
        wins= win_lose_data.get("win"),
        loses= win_lose_data.get("lose")
    )
    return(player)

def get_match_data(match_id):
    url = f"https://api.opendota.com/api/matches/{match_id}"

    match_data = get_api_request(url)

    players = match_data.get("players")

    players_data = []

    for player in players:
        player_model = Player(
            account_id = player["account_id"] if player.get("account_id") is not None else None,
            personaname = player["personaname"] if player.get("personaname") is not None else "Anonymous",
            rank_tier= player["rank_tier"] if player.get("rank_tier") is not None else 0,
            avatar_url= player.get("avatar_url"),
            kills= player["kills"],
            deaths= player["deaths"],
            assists= player["assists"],
            last_hits= player["last_hits"],
            denies= player["denies"],
            gold_per_min= player["gold_per_min"],
            xp_per_min= player["xp_per_min"],
            net_worth= player["net_worth"],
            total_gold= player["total_gold"],
            level= player["level"],
        )
        players_data.append(player_model)
    
    match = Match(
        players= players_data,
        radiant_win= match_data["radiant_win"],
        duration= match_data["duration"],
        match_id= match_id,
        game_mode= match_data["game_mode"],
        radiant_score= match_data["radiant_score"],
        dire_score= match_data["dire_score"],
        leagueid= match_data["leagueid"]
    )
    return match