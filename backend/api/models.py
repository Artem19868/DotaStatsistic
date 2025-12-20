from pydantic import BaseModel, field_validator
from typing import List, Optional,Dict

class Item(BaseModel):
    id: Optional[int] = None
    price: Optional[int] = None
    image_url: Optional[str] = None
    display_name: Optional[str] = None

class Ability(BaseModel):
    id: int
    name: str
    image_url: str
    #display_name: str

class Hero(BaseModel):
    id: int
    name: str
    image_url: str
    display_name: str
    abilities: Optional[Dict[int, Ability]] = None

class Player(BaseModel):
    steam_32_id: Optional[int] = None
    user_name: str = "Anonymous"
    avatar_url: Optional[str] = None
    win_rate: Optional[float] = None
    rank_tier: int
    hero: Optional[Hero] = None
    kills: Optional[int] = None
    deaths: Optional[int] = None
    assists: Optional[int] = None
    last_hits: Optional[int] = None
    denies: Optional[int] = None
    gold_per_min: Optional[int] = None
    xp_per_min: Optional[int] = None
    net_worth: Optional[int] = None
    total_gold: Optional[int] = None
    level: Optional[int] = None
    wins: Optional[int] = 0
    loses: Optional[int] = 0
    item_0: Optional[Item] = None
    item_1: Optional[Item] = None
    item_2: Optional[Item] = None
    item_3: Optional[Item] = None
    item_4: Optional[Item] = None
    item_5: Optional[Item] = None
    backpack_0: Optional[Item] = None
    backpack_1: Optional[Item] = None
    backpack_2: Optional[Item] = None
    item_neutral: Optional[Item] = None
    item_neutral2: Optional[Item] = None

    @field_validator("win_rate", mode="before")
    def win_rate_validate(cls, v, info):
        data = info.data
        wins = data.get("wins", 0)
        loses = data.get("loses", 0)
        total = wins + loses

        if total == 0:
            win_rate = 0
            return win_rate

        win_rate = wins / total

        return round(win_rate, 2)
    
class Match(BaseModel):
    players: List[Player]
    radiant_win: bool
    duration: int
    match_id: int
    game_mode: int
    radiant_score: int
    dire_score: int
    leagueid: int