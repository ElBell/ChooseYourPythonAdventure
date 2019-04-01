from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from ChooseYourAdventure.forms import GameForm
from ChooseYourAdventure.models import Game


def welcome(request):
    if request.user.is_authenticated:
        return redirect('player_home')
    return render(request, "ChooseYourAdventure/welcome.html",
                  {'total_games': Game.objects.count(),
                   'games': Game.objects.all()})


@login_required
def new_game(request):
    if request.method == "POST":
        game = Game(creator=request.user)
        form = GameForm(instance=game, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_home')
    else:
        form = GameForm()
    return render(request, 'ChooseYourAdventure/new_game_form.html', {'form': form})
