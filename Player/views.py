from django.shortcuts import render

# Create your views here.
from ChooseYourAdventure.models import Game


def home(request):
    return render(request, "player/home.html",
                  {'total_games': Game.objects.count(),
                   'games_by_user': Game.objects.games_by_user(request.user)})
