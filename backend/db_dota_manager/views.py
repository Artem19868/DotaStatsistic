import json

import redis
from django.shortcuts import render
from django.db import models as Models
from django.core import serializers
from django.http import JsonResponse
from django.forms import model_to_dict

from .models import Player, Hero, Item, Match
from .service import PlayerService, HeroService, HeroAbilityService, ItemService
from api.client import get_player_data_api, get_match_data_api

# Create your views here.
class RedisCache:
    def __init__(self, entity_type, entity_id) :
        self.entity_type = entity_type
        self.entity_id = entity_id

        self.entities = {
            'player': f'player:{entity_id}',
            'match': f'match:{entity_id}',
            'hero': f'hero:{entity_id}',
            'item': f'item:{entity_id}'
        }

        # Connect to Redis server
        self.redis_client = redis.Redis()
        print(self.redis_client.ping())

    def get_data_from_db(self):
        #Entity config variable
        ENTIRTY_CONFIG = {
            'player' : {
                'model': Player,
                'field': 'steam_32_id',
                'service': PlayerService(),
                'ttl': 86_400
            },
            'match': {
                'model': Match,
                'field': 'match_id',
                'service': None,
                'ttl': 86_400
            },
            'hero': {
                'model': Hero,
                'field': 'hero_id',
                'service': HeroService(),
                'ttl': 86_400
            },
            'item': {
                'model': Item,
                'field': 'item_id',
                'service': ItemService(),
                'ttl': 86_400
            }
        }
        try:

            config = ENTIRTY_CONFIG.get(self.entity_type)

            model = config['model']
            field = config['field']
            ttl = config['ttl']
            service = config['service']

            field_kwargs = {field: self.entity_id}

            # if self.entity_type == 'player':
            #     entity_data_serialize = serializers.serialize("json", Player.objects.filter(steam_32_id = self.entity_id))

            #     self.redis_client.setex(self.entities[self.entity_type], 3600, entity_data_serialize)

            #     return entity_data_serialize
            
            # elif self.entity_type == 'match':
            #     entity_data_serialize = serializers.serialize("json", Match.objects.filter(match_id = self.entity_id).get())

            #     self.redis_client.setex(self.entities[self.entity_type], 86_400, entity_data_serialize)

            #     return entity_data_serialize
            
            # if self.entity_type == 'hero':
            model_query_set = model.objects.filter(**field_kwargs)
            model_obj = model_query_set.first()

            entity_data_serialize = None
                    
            if model_query_set.exists():
                entity_data_serialize = serializers.serialize("json", [model_obj])
                print(f'If hero exixts: {entity_data_serialize}')
            else:
                #improve this code!
                if self.entity_type == 'player' or self.entity_type == 'match':
                    # data is Django model
                    data = service.get_data(self.entity_id)
                    print(f'API data: {data}')
                    
                    # dict_data = model_to_dict(data)
                    
                    # fields = [field.name for field in Player._meta.fields]
                    # filtered_data = {key: value for key, value in dict_data.items() if key in fields}
                    
                    # obj = service.create(self.entity_id, filtered_data)
                    entity_data_serialize = serializers.serialize("json", [data])
                else:
                    #hero_service = HeroService()
                    obj_data = service.get_data(self.entity_id)
                    obj = service.create(self.entity_id, obj_data)
                    entity_data_serialize = serializers.serialize("json", [obj])
                    print(f'entity_data_serialize: {entity_data_serialize}')
                


            #test
            print(f'entity_data_serialize: {entity_data_serialize}')
                
            self.redis_client.setex(self.entities[self.entity_type], ttl, entity_data_serialize)

            return entity_data_serialize
            
            # elif self.entity_type == 'item':
            #     entity_data_serialize = serializers.serialize("json", Item.objects.filter(item_id = self.entity_id).get())

            #     self.redis_client.setex(self.entities[self.entity_type], 86_400, entity_data_serialize)

            #     return entity_data_serialize
            
        except Exception as e:
            print(e)
            return None

    def get_cache_data(self):
        try:
            if self.entity_type in self.entities:

                entity_data = self.redis_client.get(self.entities[ self.entity_type ])

                if entity_data:
                    print("Connected to Redis successfully!")
                    self.redis_client.close()
                    #decode bytes
                    return entity_data.decode('utf-8')
                else:
                    print('Not in redis')
                    entity_data = self.get_data_from_db()
                    self.redis_client.close()
                    return entity_data
            else:
                print('unknown entity type!')
                self.redis_client.close()
        except redis.exceptions.ConnectionError as e:
            print(f'Connection Error: {e}')
            self.redis_client.close()
            return 0

def get_player_data(request, steam_32_id):
    # steam_32_id = request.GET.get('id')
    data = RedisCache('player', steam_32_id).get_cache_data()
    json_string = data
    return_data = json.loads(json_string)
    return JsonResponse(return_data, safe=False)

def get_match_data(request):
    match_id = request.GET.get('id')
    data = RedisCache('match', match_id).get_cache_data()
    json_string = data
    return_data = json.loads(json_string)
    return JsonResponse(return_data, safe=False)

def get_hero_data(request, hero_id):
    #hero_id = request.GET.get('id')
    data = RedisCache('hero', hero_id).get_cache_data()
    print(data)
    json_string = data
    return_data = json.loads(json_string)
    return JsonResponse(return_data, safe=False)

# urls

# /api/player/{id}
# /api/match/{id}
# /api/heroes
# /api/hero/{id}  -- ?
# /api/items 

# redis variables names

# player_{id}
# match_{id}
# heroes
# hero_{id} -- ?
# items
# item_{id} -- ?