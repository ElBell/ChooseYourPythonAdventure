from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from ChooseYourAdventure.models import Game


@login_required
def home(request):
    return render(request, "player/home.html",
                  {'total_games': Game.objects.count(),
                   'games_by_user': Game.objects.games_by_user(request.user)})
