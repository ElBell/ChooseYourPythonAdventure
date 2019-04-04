from django.urls import path, include

from player.views import home, signup

urlpatterns = [
    path('home/', home, name='player_home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup')
]
