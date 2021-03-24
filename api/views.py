from django.utils import timezone
from rest_framework import status
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     get_object_or_404)
from rest_framework.response import Response

from .models import Event, EventTrack, EventTrackRating, Track
from .serializers import (EventSerializer, EventTrackRatingSerializer,
                          EventTrackSerializer, TrackSerializer)
from .utils import PAYLOAD, URL, get_tracks, refactor_results


class TrackListView(ListCreateAPIView):
    serializer_class = None

    def list(self, request, *args, **kwargs):
        name = self.request.data.get('name')
        artist = self.request.data.get('artist')
        if name:
            data = refactor_results(get_tracks(url=URL,
                                               payload=PAYLOAD,
                                               name=name,
                                               artist=artist,
                                               limit=100))
            return Response(data)
        return Response({'detail': 'name is requirement field'})

    def create(self, request, *args, **kwargs):
        name = self.request.data.get('name')
        temp_id = self.request.data.get('temp_id')
        if not name:
            return Response({'detail': 'name is requirement field'})

        if temp_id and temp_id.isdigit():
            tracks = refactor_results(get_tracks(url=URL,
                                                 payload=PAYLOAD,
                                                 name=name,
                                                 limit=100,
                                                 artist=''))
            for track in tracks:
                if track['temp_id'] == int(temp_id):
                    artist = track['artist']
                    url = track['url']
                    saved_track = Track.objects.get_or_create(name=name,
                                                              artist=artist,
                                                              url=url)[0]
                    del track['temp_id']
                    track['id'] = saved_track.id
                    return Response(track)
        return Response(
            {'detail': 'temp_id is not correct'})


class LoadedTrackList(ListAPIView):
    serializer_class = TrackSerializer
    queryset = Track.objects.all()


class EventView(ListCreateAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class EventTrackView(ListCreateAPIView):
    serializer_class = EventTrackSerializer

    def get_queryset(self):
        return EventTrack.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        event = get_object_or_404(Event, id=self.request.data.get('event'))
        event_track = get_object_or_404(EventTrack,
                                        event=self.request.data.get('event'),
                                        track=self.request.data.get('track'))

        event.tracks.add(event_track)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class EventTrackRatingView(ListCreateAPIView):
    serializer_class = EventTrackRatingSerializer
    queryset = EventTrackRating.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
