from .models import Player, MatchPlayer, Item, Hero, HeroAbility
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

    def create(self, account_id, player_data):
        wins = player_data.wins
        loses = player_data.loses
        total = wins + loses
        win_rate = 0.0
        print(wins,loses)
        if total > 0:
            win_rate = round(wins / total, 2)

        player = Player.objects.create(steam_32_id = account_id,
                                           user_name= player_data.user_name,
                                           avatar_url= player_data.avatar_url,
                                           rank_tier= player_data.rank_tier,
                                           win_rate=  win_rate)
                                                  
        player.save()
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

    def get_data(self, account_id):
        player_data = get_player_data_api(account_id)
        print(f'player_data: {player_data}')

        is_player_exists = Player.objects.filter(steam_32_id = account_id).exists()
        print(is_player_exists)

        if is_player_exists:
            player = Player.objects.get(steam_32_id = account_id)
            return player
        else:
            player = self.create(account_id, player_data)
            return player


class HeroService:
    def __init__(self):
        pass

    def create(self, hero_id, hero_data):
        hero = Hero.objects.create(hero_id=hero_id,
                                   name = hero_data.name,
                                   display_name = hero_data.display_name)
                                                  
        hero.save()
        return hero
    

    def get_data(self, hero_id):
        hero_data = HeroManager(hero_id).get_hero_model()

        is_hero_exists = Hero.objects.filter(hero_id = hero_id).exists()

        if is_hero_exists:
            hero = Hero.objects.get(hero_id = hero_id)
            return hero
        else:
            hero = self.create(hero_id, hero_data)
            return hero
        
class HeroAbilityService:
    def __init__(self):
        pass

    def create(self, hero_id, ability_id):
        hero = Hero.objects.get(hero_id=hero_id)

        abilities = AbilityManager(hero.name).get_abilities_models()
        ability = abilities[ability_id]

        return ability
    

    def get_data(self, hero_id):
        hero = Hero.objects.get(hero_id = hero_id)
        
        #Возвращает одну абилку а не все исправить 
        for id, ability in AbilityManager(hero.name).get_abilities_models():
            is_ability_exists = HeroAbility.objects.filter(ability_id = id).exists

            if is_ability_exists:
                ability = HeroAbility.objects.get(ability_id = id)
                return ability
            else:
                ability = self.create(hero_id, id)
                return ability
            
class ItemService:
    def __init__(self):
        pass

    def create(self, item_id, item_data):
        hero = Item.objects.create(item_id=item_id,
                                   price = item_data.price,
                                   image_url = item_data.image_url,
                                   display_name= item_data.display_name,)
                                                  
        hero.save()
        return hero
    

    def get_data(self, item_id):
        item_data = ItemManager([item_id]).get_item_model(item_id)

        is_item_exists = Item.objects.filter(item_id = item_id).exists()

        if is_item_exists:
            item = Item.objects.get(item_id = item_id)
            return item
        else:
            item = self.create(item_id, item_data)
            return item