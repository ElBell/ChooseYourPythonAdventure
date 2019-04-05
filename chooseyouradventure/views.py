from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

# Create your views here.
from chooseyouradventure.forms import GameForm, UpdateForm
from chooseyouradventure.models import Game, Star

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
    liked = Star.objects.filter(game=game, user=request.user, comment='like')
    return render(request,
                  'ChooseYourAdventure/game_page.html',
                  {'game': game, 'liked': liked})


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

def log_event(request, id):
    game = get_object_or_404(Game, id=id)
    user = request.user
    event = request.POST.get('event', 'unknown')
    if event not in Star.VALID_EVENTS:
        return JsonResponse({'success': False, 'message': 'Invalid event'})
    if event == 'like':
        liked = Star.objects.filter(game=game, user=request.user, comment='like')
        if liked:
            liked.delete()
        else:
            Star.objects.create(game=game, user=request.user, comment='like')
    else:
        Star.objects.get_or_create(game=game, user=user, comment=event)
    return JsonResponse({'success': True, 'message': 'Event logged'})
