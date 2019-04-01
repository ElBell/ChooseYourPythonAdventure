from django.urls import path
from ChooseYourAdventure.views import *

urlpatterns = [
    path('new_game/', new_game, name='new_game'),
    path('details/<str:url>', game_page, name='game_page')
]
