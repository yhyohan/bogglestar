
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^game$', 'boggle.apps.core.views.game', name='game'),
    url(r"^game/(?P<id>[0-9a-f-]+)",  'boggle.apps.core.views.game_dtl', name='game_dtl'),
    url(r'^gamestats$', 'boggle.apps.core.views.gamestats', name='gamestats'),
)
