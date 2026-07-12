from django.db import models


# Create your models here.
class Player(models.Model):
    objects = models.Manager()

    steam_32_id = models.BigIntegerField(primary_key=True, verbose_name='Steam 32 ID')

    user_name = models.CharField(max_length=200, verbose_name='User name')
    avatar_url = models.URLField(null=True, blank=True, verbose_name='User avatar url')
    win_rate = models.FloatField(null=True, blank=True, verbose_name=' Win rate')
    rank_tier = models.IntegerField(null=True, blank=True, verbose_name='Rank tier')

    def __str__(self):
        return str(self.steam_32_id)
    
    class Meta:
        verbose_name = 'Player'
        verbose_name_plural = 'Players'

class Hero(models.Model):
    objects = models.Manager()

    hero_id = models.IntegerField(primary_key=True, verbose_name='Hero id')
    name = models.CharField(max_length=200, verbose_name='Hero name')
    display_name = models.CharField(max_length=200, verbose_name='Display hero name')
    image_url = models.URLField(verbose_name='Hero image url')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Hero'
        verbose_name_plural = 'Heroes'

class HeroAbility(models.Model):
    objects = models.Manager()

    hero = models.ForeignKey(Hero, on_delete=models.CASCADE, verbose_name='Hero', related_name='abilities')

    ability_id = models.IntegerField(primary_key=True, verbose_name='Ability id')
    name = models.CharField(max_length=200, verbose_name='Ability name')
    image_url = models.URLField(verbose_name='Ability image url')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name ='Ability'
        verbose_name_plural = 'Abilities'

class Item(models.Model):
    objects = models.Manager()

    item_id = models.IntegerField(primary_key=True, verbose_name='Item id')
    price = models.IntegerField(verbose_name='Item price')
    image_url = models.URLField(verbose_name='Item image url')
    display_name= models.CharField(max_length=200, verbose_name='Display item name')

    def __str__(self):
        return self.display_name
    
    class Meta:
        verbose_name ='Item'
        verbose_name_plural = 'Items'


class Match(models.Model):
    objects = models.Manager()

    match_id = models.BigIntegerField(primary_key=True, verbose_name='Match id')

    radiant_win = models.BooleanField(verbose_name="Radiant win")
    radiant_score = models.IntegerField(verbose_name='Radiant score')
    dire_score = models.IntegerField(verbose_name='Dire score')
    duration = models.IntegerField(verbose_name='Duration')

    def __str__(self):
        return str(self.match_id)
    
    class Meta:
        verbose_name ='Macth'
        verbose_name_plural = 'Matches'

class MatchPlayer(models.Model):
    objects = models.Manager()

    # возможно игроку следует дать протект
    player = models.ForeignKey(Player,on_delete=models.CASCADE, null=True, blank=True, verbose_name='Match player')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, verbose_name='match', related_name='match_players')

    hero = models.ForeignKey(Hero, on_delete=models.PROTECT, verbose_name='Player hero')
    level = models.IntegerField()

    #KDA
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()

    #Player items
    item_0 = models.ForeignKey(Item, on_delete=models.PROTECT, null=True, related_name='matchplayer_item_0', verbose_name='item_0')
    item_1 = models.ForeignKey(Item, on_delete=models.PROTECT, null=True, related_name='matchplayer_item_1', verbose_name='item_1')
    item_2 = models.ForeignKey(Item, on_delete=models.PROTECT, null=True, related_name='matchplayer_item_2', verbose_name='item_2')
    item_3 = models.ForeignKey(Item, on_delete=models.PROTECT, null=True, related_name='matchplayer_item_3', verbose_name='item_3')
    item_4 = models.ForeignKey(Item, on_delete=models.PROTECT, null=True, related_name='matchplayer_item_4', verbose_name='item_4')
    item_5 = models.ForeignKey(Item, on_delete=models.PROTECT, null=True, related_name='matchplayer_item_5', verbose_name='item_5')
    
    backpack_0 = models.ForeignKey(Item, on_delete=models.PROTECT, null=True, related_name='matchplayer_backpack_0', verbose_name='backpack_0')
    backpack_1 = models.ForeignKey(Item, on_delete=models.PROTECT, null=True, related_name='matchplayer_backpack_1', verbose_name='backpack_1')
    backpack_2 = models.ForeignKey(Item, on_delete=models.PROTECT, null=True, related_name='matchplayer_backpack_2', verbose_name='backpack_2')
    
    item_neutral = models.ForeignKey(Item, on_delete=models.PROTECT, null=True, related_name='matchplayer_item_neutral', verbose_name='item_neutral')
    item_neutral2 = models.ForeignKey(Item, on_delete=models.PROTECT, null=True, related_name='matchplayer_item_neutral2', verbose_name='item_neutral2')

    def __str__(self):
        return f'player {self.player.steam_32_id} in match with id: {self.match.match_id}' 
    
    class Meta:
        verbose_name ='MatchPlayer'
        verbose_name_plural = 'MatchPlayers'