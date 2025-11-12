from typing import List, Dict, Tuple
from models import Ability
import os
import json

class AbilityManager:
    def __init__(self, hero_name):
        self.hero_name = hero_name

        self.heroes_abilities_data = self._load_heroes_abilities()
        #row data
        self._abilities_ids_data = self._load_abilities_ids()

        self.heroes_abilities_by_name = {}
        self._create_ability_name_mapping()

    def _load_heroes_abilities(self):
        heroes_abilities_path = os.path.join(os.path.dirname(__file__), "constants", "heroes_abilities.json")
        with open(heroes_abilities_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
                
    def _load_abilities_ids(self) -> List[Tuple[str, Dict]]:
        abilities_ids_path = os.path.join(os.path.dirname(__file__), "constants", "ability_ids.json")
        with open(abilities_ids_path, 'r', encoding="utf-8") as f:
            data = json.load(f)
            return list(data.items())

    def _create_ability_name_mapping(self):
        self.heroes_abilities_by_name = {ability_name: ability_id for ability_id, ability_name in self._abilities_ids_data}

    def _load_hero_ability_photo(self, ability):
        if ability == "generic_hidden":
            return ""   
        image_url = f"https://cdn.dota2.com/apps/dota2/images/abilities/{ability}_full.png"
        return image_url

    def get_abilities_models(self):
        abilities_models = []
        hero_data = self.heroes_abilities_data.get(self.hero_name)
        abilities_list = hero_data.get("abilities")
        for ability in abilities_list:
            ability = Ability(
                id= self.heroes_abilities_by_name.get(ability),
                name= ability,
                image_url= self._load_hero_ability_photo(ability)
            )
            abilities_models.append(ability)
        
        print(abilities_models)
        return abilities_models