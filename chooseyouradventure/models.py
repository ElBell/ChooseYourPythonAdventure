from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.encoding import smart_bytes

import base64

# Create your models here.


class GamesQuerySet(models.QuerySet):
    def games_by_user(self, user):
        return self.filter(
            creator=user
        )

    def games_by_genre(self, keyword):
        return self.filter(
            keyword=keyword
        )


class Keyword(models.Model):
    word = models.CharField(max_length=30)

    def __str__(self):
        return self.word


class Game(models.Model):
    title = models.CharField(max_length=100, help_text='Pick a snazzy title')
    creator = models.ForeignKey(User, related_name="creator", null=True, on_delete=models.SET_NULL)
    description = models.CharField(blank=True, max_length=250)
    code = models.TextField(null=True, help_text='Add your game code here')
    url = models.CharField(max_length=200, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    keywords = models.ManyToManyField(Keyword, verbose_name="list of keywords")
    objects = GamesQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('game_page', args=[self.id])

    def __str__(self):
        return "{} by {}".format(self.title, self.creator)

    def count_stars(self, event):
        return len(Star.objects.filter(game=self.id, comment=event))

    def count_views(self):
        return self.count_stars('view')
    def count_starts(self):
        return self.count_stars('start')
    def count_likes(self):
        return self.count_stars('like')


class Progress(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(User, related_name="player", on_delete=models.CASCADE)
    state = models.TextField

    def __str__(self):
        return "{}: {}".format(self.player, self.game)


class Star(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    comment = models.CharField(max_length=255)

    VALID_EVENTS = ('like', 'view', 'start', 'stop', 'continue')

    def __str__(self):
        return "{}: {}".format(self.game, self.user)
