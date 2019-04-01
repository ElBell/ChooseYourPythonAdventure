from django.contrib.auth.models import User
from django.db import models

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
    title = models.CharField(max_length=100)
    creator = models.ForeignKey(User, related_name="creator", null=True, on_delete=models.SET_NULL)
    description = models.CharField(blank=True, max_length=250)
    code = models.TextField
    url = models.CharField(max_length=200)
    date_created = models.DateTimeField
    date_modified = models.DateTimeField
    keywords = models.ManyToManyField(Keyword, verbose_name="list of keywords")
    objects = GamesQuerySet.as_manager()

    def __str__(self):
        return "{} by {}".format(self.title, self.creator)


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

    def __str__(self):
        return "{}: {}".format(self.game, self.user)
