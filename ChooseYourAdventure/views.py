from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from ChooseYourAdventure.forms import GameForm
from ChooseYourAdventure.models import Game


def welcome(request):
    if request.user.is_authenticated:
        return redirect('player_home')
    return render(request, "ChooseYourAdventure/../templates/welcome.html",
                  {'total_games': Game.objects.count(),
                   'games': Game.objects.all()})


@login_required
def new_game(request):
    form = GameForm()
    return render(request, 'ChooseYourAdventure/new_game_form.html', {'form': form})
