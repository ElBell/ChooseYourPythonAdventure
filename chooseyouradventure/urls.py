from django.urls import path
from chooseyouradventure.views import *

urlpatterns = [
    path('new_game/', new_game, name='new_game'),
    path('details/<id>', game_page, name='game_page'),
    path('edit/<id>', edit_game, name='edit_game')
]
