from django.urls import path
from django.views.decorators.cache import cache_page

from api.views import (EventTrackRatingView, EventTrackView, EventView,
                       LoadedTrackList, TrackListView)

urlpatterns = [
    path('tracks/loaded/', cache_page(1 * 10)(LoadedTrackList.as_view())),
    path('tracks/', cache_page(1 * 10)(TrackListView.as_view())),
    path('events/tracks/', EventTrackView.as_view()),
    path('events/', EventView.as_view()),
    path('ratings/', EventTrackRatingView.as_view()),
]
