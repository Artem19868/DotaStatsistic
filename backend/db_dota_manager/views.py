import json

import redis
from django.shortcuts import render
from django.db import models as Models
from django.core import serializers
from django.http import JsonResponse
from django.forms import model_to_dict

from .models import Player, Hero, Item, Match
from .service import PlayerService, HeroService, HeroAbilityService, ItemService, MatchService, MatchPlayerService
from api.client import get_player_data_api, get_match_data_api

# Create your views here.
class RedisCache:
    #Entity config variable
    ENTITY_CONFIG = {
        'player' : {
            'model': Player,
            'field': 'steam_32_id',
            'service': PlayerService,
            'ttl': 86_400
        },
        'match': {
            'model': Match,
            'field': 'match_id',
            'service': MatchService,
            'ttl': 86_400
        },
        'hero': {
            'model': Hero,
            'field': 'hero_id',
            'service': HeroService,
            'ttl': 86_400
        },
        'item': {
            'model': Item,
            'field': 'item_id',
            'service': ItemService,
            'ttl': 86_400
        }
            }
    
    ENTITIES_CONFIG = {
        'heroes':{
            'model': Hero,
            'ttl': 86_400
        },
        'items':{
            'model': Item,
            'ttl': 86_400
        }
    }
    
    def __init__(self, entity_type, entity_id) :
        self.entity_type = entity_type
        self.entity_id = entity_id
        
        self.entity_data_serialize = None
        
        
        self.cache_key = f'{self.entity_type}:all' if self.entity_type in self.ENTITIES_CONFIG else f'{self.entity_type}:{self.entity_id}'

        # Connect to Redis server
        self.redis_client = redis.Redis()
        print(self.redis_client.ping())
    
    def get_object_from_db(self):
        try:
            config = self.ENTITY_CONFIG.get(self.entity_type)
            model = config['model']
            field = config['field']
            ttl = config['ttl']
            service = config['service']()

            field_kwargs = {field: self.entity_id}
            
            model_obj = model.objects.filter(**field_kwargs).first()
                    
            if model_obj is None:
                model_obj = service.get_or_create(self.entity_id)
            
            data = [model_obj]
            
            if self.entity_type == 'match':
                data += list(MatchPlayerService().get_all(self.entity_id))
            
            self.entity_data_serialize = serializers.serialize("json", data)
                
            self.redis_client.setex(self.cache_key, ttl, self.entity_data_serialize) 
            return self.entity_data_serialize
            
        except Exception as e:
            print(f'Exeption in get_object_from_db:  {e}')
            return None
        
    def get_objects_from_db(self):
            try:
                config = self.ENTITIES_CONFIG.get(self.entity_type)
                model = config['model']
                ttl = config['ttl']
                
                model_objects = model.objects.all()
                
                self.entity_data_serialize = serializers.serialize("json", model_objects)
                print(self.entity_data_serialize)
                    
                self.redis_client.setex(self.cache_key, ttl, self.entity_data_serialize) 
                return self.entity_data_serialize
                
            except Exception as e:
                print(f'Exeption in get_objects_from_db:  {e}')
                return None
        
    def get_cache_data(self):
        try:
            if self.entity_type in self.ENTITY_CONFIG or self.entity_type in self.ENTITIES_CONFIG:

                entity_data = self.redis_client.get(self.cache_key)

                if entity_data:
                    print("Connected to Redis successfully!")
                    self.redis_client.close()
                    #decode bytes
                    return entity_data.decode('utf-8')
                else:
                    print('Not in redis')
                    if self.entity_type in self.ENTITIES_CONFIG:
                        entity_data = self.get_objects_from_db()
                    else:
                        entity_data = self.get_object_from_db() 
                    self.redis_client.close()
                    return entity_data
            else:
                print('unknown entity type!')
                self.redis_client.close()
        except redis.exceptions.ConnectionError as e:
            print(f'Connection Error: {e}')
            self.redis_client.close()
            return None

def get_player_data(request, steam_32_id):
    data = RedisCache('player', steam_32_id).get_cache_data()
    json_string = data
    return_data = json.loads(json_string)
    return JsonResponse(return_data, safe=False)

def get_match_data(request,match_id):
    data = RedisCache('match', match_id).get_cache_data()
    json_string = data
    return_data = json.loads(json_string)
    return JsonResponse(return_data, safe=False)

def get_hero_data(request, hero_id):
    data = RedisCache('hero', hero_id).get_cache_data()
    json_string = data
    return_data = json.loads(json_string)
    return JsonResponse(return_data, safe=False)

def get_all_heroes_data(request):
    data = RedisCache('heroes', None).get_cache_data()
    json_string = data
    return_data = json.loads(json_string)
    return JsonResponse(return_data, safe=False)