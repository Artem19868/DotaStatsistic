from typing import List, Dict
from models import Hero
import os
import json
from abilities import AbilityManager

class HeroManager:
    def __init__(self):
        self.heroes_data = self._load_heroes()
        self.heroes_by_id = {}
        self._create_id_mapping()

    def _load_heroes(self) -> List[Dict]:
        heroes_path = os.path.join(os.path.dirname(__file__), "constants", "heroes.json")
        with open(heroes_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return list(data.values())                

    def _create_id_mapping(self):
        self.heroes_by_id = { hero["id"]:hero for hero in self.heroes_data}
        
    def _load_hero_photo(self, hero_name):
        image_url = f"https://cdn.dota2.com/apps/dota2/images/heroes/{hero_name.replace('npc_dota_hero_', '')}_full.png"
        return image_url

    def get_hero_model(self, hero_id: int):
        hero = self.heroes_by_id.get(hero_id)
        hero_model = Hero(id=hero_id,
                          name=hero["name"],
                          image_url=self._load_hero_photo(hero["name"]),
                          display_name=hero["localized_name"],
                          abilities= AbilityManager(hero["name"]).get_abilities_models()
                          )
        print(hero_model)
        return hero_model

hero = HeroManager()

hero.get_hero_model(42)