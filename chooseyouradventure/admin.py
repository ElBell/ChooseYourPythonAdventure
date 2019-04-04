from django.contrib import admin

# Register your models here.
from chooseyouradventure.models import *


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'description')


admin.site.register(Keyword)
admin.site.register(Star)
admin.site.register(Progress)

