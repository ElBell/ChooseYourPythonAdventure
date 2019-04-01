from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from ChooseYourAdventure.models import Game


@login_required
def home(request):
    return render(request, "player/home.html",
                  {'total_games': Game.objects.count(),
                   'games_by_user': Game.objects.games_by_user(request.user)})


def signup(request):
    if request.user.is_authenticated:
        return redirect('player_home')
    return render(request, "Player/signup.html")
