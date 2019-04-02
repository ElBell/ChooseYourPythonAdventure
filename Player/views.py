from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic

from ChooseYourAdventure.models import Game
from Player.forms import SignUpForm


@login_required
def home(request):
    return render(request, "player/home.html",
                  {'games_by_user': Game.objects.games_by_user(request.user),
                   'num_player_games':  Game.objects.games_by_user(request.user).count()})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('player_home')
    else:
        form = SignUpForm()
    return render(request, 'Player/signup.html', {'form': form})
