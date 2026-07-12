from .models import Player, MatchPlayer, Item, Hero, HeroAbility, Match
from api import HeroManager, AbilityManager, ItemManager, get_player_data_api, get_match_data_api

def model_to_tuple(obj):
    try:
        return tuple(obj.dict().items())
    except AttributeError:
        try:
            return tuple((field.name, getattr(obj, field.name)) for field in obj._meta.fields)
        except AttributeError:
            raise TypeError('Not Django or Pydantic model')

class PlayerService:
    def __init__(self):
        pass

    def _create(self, account_id, player_data):
        wins = player_data.wins
        loses = player_data.loses
        total = wins + loses
        win_rate = 0.0
        
        if total > 0:
            win_rate = round(wins / total, 2)

        player = Player.objects.create(steam_32_id = account_id,
                                           user_name= player_data.user_name,
                                           avatar_url= player_data.avatar_url,
                                           rank_tier= player_data.rank_tier,
                                           win_rate=  win_rate)
                                                  
        player.save()
        return player
    
    def get(self, account_id):
        player = Player.objects.get(steam_32_id = account_id)
        return player
    
    def update_data(self, account_id, player_data):
        player = Player.objects.get(steam_32_id = account_id)

        django_player = model_to_tuple(player)
        pydantic_player = model_to_tuple(player_data)

        new_model_values = {}
        for (django_key, django_value), (pydantic_key, pydantic_value) in zip(django_player, pydantic_player):
            if django_key == pydantic_key and django_value != pydantic_value:
                new_model_values[django_key] = pydantic_value
    
        Player.objects.filter(steam_32_id = account_id).update(**new_model_values)

        updated_player = Player.objects.get(steam_32_id = account_id)
        return updated_player

    def get_or_create(self, account_id):
        player_data = get_player_data_api(account_id)

        is_player_exists = Player.objects.filter(steam_32_id = account_id).exists()

        if is_player_exists:
            player = self.get(account_id)
            return player
        else:
            player = self.create(account_id, player_data)
            return player

class HeroService:
    def __init__(self):
        pass

    def _create(self, hero_id, hero_data):
        hero = Hero.objects.create(hero_id=hero_id,
                                   name = hero_data.name,
                                   display_name = hero_data.display_name,
                                   image_url = hero_data.image_url)
                                                  
        hero.save()
        return hero
    
    def get(self,hero_id):
        hero = Hero.objects.get(hero_id = hero_id)
        return hero
    
    def get_or_create(self, hero_id):
        hero_data = HeroManager(hero_id).get_hero_model()

        is_hero_exists = Hero.objects.filter(hero_id = hero_id).exists()

        if is_hero_exists:
            hero = self.get(hero_id)
            return hero
        else:
            hero = self.create(hero_id, hero_data)
            return hero
                
class HeroAbilityService:
    def __init__(self):
        pass

    def _create(self, hero_id, ability_id):
        hero = Hero.objects.get(hero_id=hero_id)

        abilities = AbilityManager(hero.name).get_abilities_models()
        ability = abilities[ability_id]
        django_ability = HeroAbility.objects.create(hero = Hero.objects.get(hero_id=hero_id),
                                                    ability_id = ability.id,
                                                    name = ability.name,
                                                    image_url = ability.image_url)
        
        django_ability.save()

        return django_ability
    
    def get(self, ability_id):
        ability = HeroAbility.objects.get(ability_id = ability_id)
        return ability

    def get_or_create(self, hero_id):
        hero = Hero.objects.get(hero_id = hero_id)
        abilities = []
        
        for id, ability in AbilityManager(hero.name).get_abilities_models().items():
            is_ability_exists = HeroAbility.objects.filter(ability_id = id).exists()

            if is_ability_exists:
                ability = self.get(id)
                abilities.append(ability)
            else:
                ability = self.create(hero_id, id)
                abilities.append(ability)
            
        #return all hero abilities
        return abilities
            
class ItemService:
    def __init__(self):
        pass

    def _create(self, item_id, item_data):
        item = Item.objects.create(item_id=item_id,
                                   price = item_data.price,
                                   image_url = item_data.image_url,
                                   display_name= item_data.display_name,)
                                                  
        item.save()
        return item
    
    def get(self, item_id):
        item = Item.objects.get(item_id = item_id)
        return item

    def get_or_create(self, item_id):
        item_data = ItemManager([item_id]).get_item_model(item_id)

        is_item_exists = Item.objects.filter(item_id = item_id).exists()

        if is_item_exists:
            item = self.get(item_id)
            return item
        else:
            item = self.create(item_id, item_data)
            return item
        
    def ensure_items_exist(self, player_dict):
        item_fields = ['item_0', 'item_1', 'item_2', 'item_3', 'item_4', 'item_5',
                            'backpack_0', 'backpack_1', 'backpack_2',
                            'item_neutral', 'item_neutral2']
            
        for item_field in item_fields:
            item_data = player_dict.get(item_field)
                
            if not item_data:
                continue
            if item_data.get('id') is None:
                continue
                
            item_id = item_data.get('id')
            
            if not Item.objects.filter(item_id = item_id).exists():
                #create item in db
                self.get_or_create(item_id)
        
    def items_ids(self, player_dict):
        item_fields = ['item_0', 'item_1', 'item_2', 'item_3', 'item_4', 'item_5',
                            'backpack_0', 'backpack_1', 'backpack_2',
                            'item_neutral', 'item_neutral2']
        ids = [] 
        for item_field in item_fields:
            item_data = player_dict.get(item_field)
                
            if not item_data:
                item_id = None
            else:  
                item_id = item_data.get('id')
            ids.append(item_id)
            
        return ids

class MatchPlayerService:
    def __init__(self):
        self.item_service = ItemService()
        self.hero_service = HeroService()
        self.hero_ability_service = HeroAbilityService()
        self.player_service = PlayerService()
    
    def get_all(self, match_id):
        is_match_exists = Match.objects.filter(match_id = match_id).exists()

        if is_match_exists:
            match = Match.objects.get(match_id = match_id)
            return match.match_players.all()
        
        print('Match does not exist')
        return None
    
    def _create(self, player_data, match):            
        player_dict = player_data.dict()
                
        # Add to the db if it's not already there.        
        self.item_service.ensure_items_exist(player_dict)
        self.hero_service.get_or_create(player_data.hero.id)
        self.hero_ability_service.get_or_create(player_data.hero.id)
        self.player_service.get_or_create(player_data.steam_32_id)
                
        player_items_ids = self.item_service.items_ids(player_dict)
               
        django_match_player = MatchPlayer.objects.create(player= Player.objects.filter(steam_32_id = player_data.steam_32_id).first(),
                                                        match= match,
                                                        hero= Hero.objects.get(hero_id = player_data.hero.id),
                                                        level= player_data.level,
                                                
                                                        #KDA
                                                        kills= player_data.kills,
                                                        deaths= player_data.deaths,
                                                        assists= player_data.assists,
                                                
                                                        #Player items
                                                        item_0= Item.objects.filter(item_id = player_items_ids[0]).first(),
                                                        item_1= Item.objects.filter(item_id = player_items_ids[1]).first(),
                                                        item_2= Item.objects.filter(item_id = player_items_ids[2]).first(),
                                                        item_3= Item.objects.filter(item_id = player_items_ids[3]).first(),
                                                        item_4= Item.objects.filter(item_id = player_items_ids[4]).first(),
                                                        item_5= Item.objects.filter(item_id = player_items_ids[5]).first(),
                                                        
                                                        backpack_0= Item.objects.filter(item_id = player_items_ids[6]).first(),
                                                        backpack_1= Item.objects.filter(item_id = player_items_ids[7]).first(),
                                                        backpack_2= Item.objects.filter(item_id = player_items_ids[8]).first(),
                                                        
                                                        item_neutral= Item.objects.filter(item_id = player_items_ids[9]).first(),
                                                        item_neutral2= Item.objects.filter(item_id = player_items_ids[10]).first())
        django_match_player.save() 
        
    def create_all(self, players_data, match_id):
        match = Match.objects.get(match_id = match_id)
        for player_data in players_data:
            self.create(player_data, match)            
        
class MatchService:
    def __init__(self):
        self.match_player_service = MatchPlayerService()
    
    def get(self, match_id):
        match = Match.objects.get(match_id = match_id)
        return match
    
    def _create(self, match_id, match_data):
        try:
            
            match = Match.objects.create(match_id= match_id,
                                        radiant_win= match_data.radiant_win,
                                        radiant_score= match_data.radiant_score,
                                        dire_score= match_data.dire_score,
                                        duration= match_data.duration)
            match.save()
            
            self.match_player_service.create_all(match_data.players, match_id)
                
            return match
        except Exception as e:
            print(f"Exeption in create(): {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_or_create(self, match_id):
        match_data = get_match_data_api(match_id)

        is_match_exists = Match.objects.filter(match_id = match_id).exists()

        if is_match_exists:
            match = self.get(match_id)
            return match
        else:
            match = self.create(match_id, match_data)
            return match