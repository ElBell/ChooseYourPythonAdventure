from django.urls import path
from ChooseYourAdventure.views import new_game

urlpatterns = [
    path('new_game/', new_game, name='new_game'),
]
