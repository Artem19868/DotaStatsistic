from pydantic import BaseModel, field_validator
from typing import List, Optional

class Player(BaseModel):
    account_id: Optional[int] = None
    personaname: str
    rank_tier: str
    avatar_url: str
    kills: int
    deaths: int
    assists: int
    last_hits: int
    denies: int
    gold_per_min: int
    xp_per_min: int
    net_worth: int
    total_gold: int
    level: int
    wins: int
    loses: int
    win_rate: Optional[float] = None

    @field_validator("win_rate", mode="before")
    def win_rate_validate(cls, v, info):
        data = info.data
        wins = data.get("wins", 0)
        loses = data.get("loses", 0)
        total = wins + loses

        win_rate = wins / total

        return round(win_rate, 2)
    
    @field_validator("personaname", mode="before")
    def personaname_validate(cls, v, info):
        data = info.data
        if data.get("account_id") == None:
            return "Anonymous"

class Match(BaseModel):
    players: List[Player]
    radiant_win: bool
    duration: int
    match_id: int
    game_mode: int
    radiant_score: int
    dire_score: int
    leagueid: int

class Items(BaseModel):
    id: int
    name: str
    image_url: str
    display_name: str

class Ability(BaseModel):
    id: int
    name: str
    image_url: str
    display_name: str

class Hero(BaseModel):
    id: int
    name: str
    image_url: str
    display_name: str
    abilities: List[Ability]

