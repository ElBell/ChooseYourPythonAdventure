from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from ChooseYourAdventure.forms import GameForm, UpdateForm
from ChooseYourAdventure.models import Game


def welcome(request):
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


def game_page(request, id):
    game = get_object_or_404(Game, id=id)
    return render(request,
                  'ChooseYourAdventure/game_page.html',
                  {'game': game})


def edit_game(request, id):
    game = get_object_or_404(Game, id=id)
    if request.user == game.creator:
        form = UpdateForm(request.POST or None, instance=game)
        if form.is_valid():
            form.save()
            return redirect('player_home')
        return render(request, 'ChooseYourAdventure/edit_game.html', {'form': form,
                                                                      'game': game})
    else:
        return render(request,
                      'ChooseYourAdventure/game_page.html',
                      {'game': game})
