from django.shortcuts import render

# Create your views here.
from ChooseYourAdventure.models import Game


def welcome(request):
    return render(request, "ChooseYourAdventure/welcome.html",
                  {'games': Game.objects.all()})
