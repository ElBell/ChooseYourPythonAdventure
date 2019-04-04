from django.forms import ModelForm

from chooseyouradventure.models import Game


class GameForm(ModelForm):
    class Meta:
        model = Game
        exclude = ('creator', 'date_created', 'date_modified')


class UpdateForm(ModelForm):
    class Meta:
        model = Game
        exclude = ('creator', 'date_created', 'date_modified')
