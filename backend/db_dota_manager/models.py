from django.db import models


# Create your models here.
class Player(models.Model):
    objects = models.Manager()

    steam_32_id = models.BigIntegerField(primary_key=True, verbose_name='Steam 32 ID')

    user_name = models.CharField(max_length=200, verbose_name='User name')
    avatar_url = models.URLField(verbose_name='User avatar url')
    win_rate = models.FloatField()
    rank_tier = models.IntegerField(verbose_name='Rank tier')

    def __str__(self):
        return self.steam_32_id
    
    class Meta:
        verbose_name = 'Player'
        verbose_name_plural = 'Players'

class Hero(models.Model):
    objects = models.Manager()

    hero_id = models.IntegerField(primary_key=True, verbose_name='Hero id')
    name = models.CharField(max_length=200, verbose_name='Hero name')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Hero'
        verbose_name_plural = 'Heroes'

class HeroAbility(models.Model):
    objects = models.Manager()

    hero_id = models.ForeignKey(Hero,on_delete=models.CASCADE,verbose_name='Hero id', related_name='abilities')
    ability_id = models.IntegerField(primary_key=True,verbose_name='Ability id')

    name = models.CharField(max_length=200, verbose_name='Ability name')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name ='Ability'
        verbose_name_plural = 'Abilities'

class Item(models.Model):
    objects = models.Manager()

    item_id = models.IntegerField(primary_key=True, verbose_name='Item id')
    name = models.CharField(max_length=200, verbose_name='Item name')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name ='Item'
        verbose_name_plural = 'Items'


class Match(models.Model):
    objects = models.Manager()

    match_id = models.BigIntegerField(primary_key=True,verbose_name='Match id')

    radiant_win = models.BooleanField(verbose_name="Radiant win")
    radiant_score = models.IntegerField(verbose_name='Radiant score')
    dire_score = models.IntegerField(verbose_name='Dire score')
    duration = models.IntegerField(verbose_name='Duration')

    def __str__(self):
        return self.match_id
    
    class Meta:
        verbose_name ='Macth'
        verbose_name_plural = 'Matches'

class MatchPlayer(models.Model):
    objects = models.Manager()

    player = models.ForeignKey(Player,on_delete=models.CASCADE,null=True,blank=True, verbose_name='Match player',related_name='players')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, verbose_name='match')

    hero = models.ForeignKey(Hero, on_delete=models.PROTECT, verbose_name='Player hero')
    level = models.IntegerField()

    #KDA
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()

    #Player items
    item_0 = models.ForeignKey(Item, on_delete=models.PROTECT,verbose_name='item_0')
    item_1 = models.ForeignKey(Item, on_delete=models.PROTECT,verbose_name='item_1')
    item_2 = models.ForeignKey(Item, on_delete=models.PROTECT,verbose_name='item_2')
    item_3 = models.ForeignKey(Item, on_delete=models.PROTECT,verbose_name='item_3')
    item_4 = models.ForeignKey(Item, on_delete=models.PROTECT,verbose_name='item_4')
    item_5 = models.ForeignKey(Item, on_delete=models.PROTECT,verbose_name='item_5')
    backpack_0 = models.ForeignKey(Item, on_delete=models.PROTECT,verbose_name='backpack_0')
    backpack_1 = models.ForeignKey(Item, on_delete=models.PROTECT,verbose_name='backpack_1')
    backpack_2 = models.ForeignKey(Item, on_delete=models.PROTECT,verbose_name='backpack_2')
    item_neutral = models.ForeignKey(Item, on_delete=models.PROTECT,verbose_name='item_neutral')
    item_neutral2 = models.ForeignKey(Item, on_delete=models.PROTECT,verbose_name='item_neutral2')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name ='MatchPlayer'
        verbose_name_plural = 'MatchPlayers'