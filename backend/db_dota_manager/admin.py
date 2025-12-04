from django.contrib import admin
from .models import Player, MatchPlayer, Match, Hero, HeroAbility, Item

# Register your models here.
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('steam_32_id', 'user_name', 'rank_tier')
    search_fields = ('steam_32_id', 'user_name')
    list_per_page = 20
    list_max_show_all = 100

class MatchPlayerAdmin(admin.ModelAdmin):
    list_display = ('player', 'hero', 'match__match_id')
    search_fields = ('match__match_id')
    list_per_page = 20
    list_max_show_all = 100

class MatchAdmin(admin.ModelAdmin):
    list_display = ('match_id', 'radiant_win', 'radiant_score', 'dire_score', 'duration')
    search_fields = ('match_id')
    list_per_page = 20
    list_max_show_all = 100

class HeroAdmin(admin.ModelAdmin):
    list_display = ('hero_id', 'name')
    search_fields = ('hero_id', 'name')
    list_per_page = 20
    list_max_show_all = 100

class HeroAbilityAdmin(admin.ModelAdmin):
    list_display = ('ability_id', 'hero_id' ,'name')
    search_fields = ('hero_id', 'name')
    list_per_page = 20
    list_max_show_all = 100

class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_id','name')
    search_fields = ('item_id', 'name')
    list_per_page = 20
    list_max_show_all = 100

admin.site.register(Player, PlayerAdmin)
admin.site.register(MatchPlayer, MatchPlayerAdmin)
admin.site.register(Hero, HeroAdmin)
admin.site.register(HeroAbility, HeroAbilityAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Item, ItemAdmin)
