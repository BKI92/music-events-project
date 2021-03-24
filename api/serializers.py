from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Event, EventTrack, EventTrackRating, Track


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Track


class EventTrackSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField('get_rating', default=0)
    serializers.SerializerMethodField('ordering_by')

    # def validate(self, attrs):
    #     event_id = attrs.get('event')
    #     # track = self.context['track'].user
    #     event = get_object_or_404(Event, id=event_id)
    #     if event.max_tracks <= event.tracks.count():
    #         raise serializers.ValidationError(
    #             {'retry error': 'You have already voted on this track'})
    #     if event.time_limit < timezone.now():
    #         raise serializers.ValidationError(
    #             {'detail': 'The time for adding tracks to this event is over.'})
    #
    #     return attrs

    class Meta:
        model = EventTrack
        fields = ('id', 'event', 'track', 'rating',)

    @staticmethod
    def get_rating(obj):
        ratings = EventTrackRating.objects.filter(event_track=obj.id)
        if ratings:
            total_rating = [rating.score for rating in ratings]
            avg_rating = round(sum(total_rating) / len(total_rating), 2)
            return avg_rating
        return 0

    def validate(self, attrs):
        event_id = attrs.get('event').id
        track_id = attrs.get('track').id
        event = get_object_or_404(Event, id=event_id)
        if EventTrack.objects.filter(event=event_id, track=track_id):
            raise serializers.ValidationError(
                {'retry error': 'This track on current Event already exist.'})

        if event.max_tracks <= event.tracks.count():
            raise serializers.ValidationError(
                {'retry error': 'The maximum number of tracks has been reached '
                                'on this event '})
        if event.time_limit < timezone.now():
            raise serializers.ValidationError(
                {'detail': 'The time for adding tracks to this event is over.'})

        return attrs


class EventSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    tracks = EventTrackSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'time_limit', 'max_tracks', 'author', 'tracks')


class EventTrackRatingSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    def validate(self, attrs):
        event_track = attrs.get('event_track')
        user = self.context['request'].user
        if EventTrackRating.objects.filter(event_track=event_track, user=user):
            raise serializers.ValidationError(
                {'retry error': 'You have already voted on this track&'})

        return attrs

    class Meta:
        model = EventTrackRating
        fields = ('id', 'event_track', 'user', 'score',)
