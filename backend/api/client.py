import requests
from models import Player, Match
from items import ItemManager
from heroes import HeroManager

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
        items_ids = [player["item_0"],
                     player["item_1"],
                     player["item_2"],
                     player["item_3"],
                     player["item_4"],
                     player["item_5"],
                     player["backpack_0"],
                     player["backpack_1"],
                     player["backpack_2"],
                     player["item_neutral"],
                     player["item_neutral2"],]
        
        item_manager = ItemManager(items_ids)
        hero_manager = HeroManager(player["hero_id"])

        player_items = [item_manager.get_item_model(id) for id in item_manager.items_ids]

        player_model = Player(
            account_id = player["account_id"] if player.get("account_id") is not None else None,
            personaname = player["personaname"] if player.get("personaname") is not None else "Anonymous",
            rank_tier= player["rank_tier"] if player.get("rank_tier") is not None else 0,
            avatar_url= player.get("avatar_url"),
            hero = hero_manager.get_hero_model(),
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
            item_0=player_items[0],
            item_1=player_items[1],
            item_2=player_items[2],
            item_3=player_items[3],
            item_4=player_items[4],
            item_5=player_items[5],
            backpack_0=player_items[6],
            backpack_1=player_items[7],
            backpack_2=player_items[8],
            item_neutral=player_items[9],
            item_neutral2=player_items[10],
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