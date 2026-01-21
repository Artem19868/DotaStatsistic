import json

import redis
from django.shortcuts import render
from django.db import models
from django.core import serializers

from models import Player, Hero, Item, Match

# Create your views here.
class RedisCache:
    def __init__(self, entity_type, entity_id) :
        self.entities = {
            'player': f'player:{entity_id}',
            'match': f'match:{entity_id}',
            'hero': f'hero:{entity_id}',
            'item': f'item:{entity_id}'
        }
        self.entity_type = entity_type
        self.entity_id = entity_id
        # Connect to Redis server
        self.redis_client = redis.Redis()

    def get_data_from_db(self):
        try:
            if self.entity_type == 'player':
                entity_data_serialize = serializers.serialize("json", Player.objects.filter(steam_32_id = self.entity_id).get())

                self.redis_client.setex(self.entities[self.entity_type], 3600, entity_data_serialize)

                return entity_data_serialize
            
            elif self.entity_type == 'match':
                entity_data_serialize = serializers.serialize("json", Match.objects.filter(match_id = self.entity_id).get())

                self.redis_client.setex(self.entities[self.entity_type], 86_400, entity_data_serialize)

                return entity_data_serialize
            
            elif self.entity_type == 'hero':
                entity_data_serialize = serializers.serialize("json", Hero.objects.filter(hero_id = self.entity_id).get())
                
                self.redis_client.setex(self.entities[self.entity_type], 86_400, entity_data_serialize)

                return entity_data_serialize
            
            elif self.entity_type == 'item':
                entity_data_serialize = serializers.serialize("json", Item.objects.filter(item_id = self.entity_id).get())

                self.redis_client.setex(self.entities[self.entity_type], 86_400, entity_data_serialize)

                return entity_data_serialize
            
        except models.Model.DoesNotExist:
            print('Entity does not exist')
            return None

    def get_cache_data(self):
        try:
            if self.entity_type in self.entities:

                entity_data = self.redis_client.get(self.entities[ self.entity_type ])

                if entity_data:
                    print("Connected to Redis successfully!")
                    self.redis_client.close()
                    return entity_data
                else:
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

def get_player_data(request):
    steam_32_id = request.GET.get('id')
    data = RedisCache('player', steam_32_id).get_cache_data()
    return data 

def get_match_data(request):
    match_id = request.GET.get('id')
    data = RedisCache('player', match_id).get_cache_data()
    return data 

def get_hero_data(request):
    hero_id = request.GET.get('id')
    data = RedisCache('player', hero_id).get_cache_data()
    return data