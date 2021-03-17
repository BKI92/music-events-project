from django.contrib import admin

from api.models import Event, EventTrack, EventTrackRating, Track


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'time_limit', 'max_tracks',)
    search_fields = ('title', 'time_limit', 'max_tracks',)
    list_filter = ('title', 'time_limit', 'max_tracks',)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'artist')
    search_fields = ('name', 'artist')
    list_filter = ('name', 'artist')


@admin.register(EventTrack)
class EventTrackAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'track',)
    search_fields = ('event', 'track')
    list_filter = ('event', 'track')


@admin.register(EventTrackRating)
class EventTrackRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_track', 'score')
    search_fields = ('score',)
    list_filter = ('score',)
