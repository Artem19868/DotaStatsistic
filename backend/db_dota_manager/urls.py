from django.urls import path
from. import views

urlpatterns = [
    path('player/<int:steam_32_id>/', views.get_player_data, name="get_player_data"),
    path('match/<int:match_id>/', views.get_match_data, name="get_match_data"),
    path('hero/<int:hero_id>', views.get_hero_data, name="get_hero_data")
]