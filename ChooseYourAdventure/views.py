from django.shortcuts import render, redirect

# Create your views here.
from ChooseYourAdventure.models import Game


def welcome(request):
    if request.user.is_authenticated:
        return redirect('player_home')
    return render(request, "ChooseYourAdventure/welcome.html",
                  {'total_games': Game.objects.count(),
                   'games': Game.objects.all()})
