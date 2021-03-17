from rest_framework import serializers

from .models import Event, EventTrack, EventTrackRating, Track


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Track


class EventTrackSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField('get_rating', default=0)
    serializers.SerializerMethodField('ordering_by')

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
        event = attrs.get('event').id
        track = attrs.get('track').id
        if EventTrack.objects.filter(event=event, track=track):
            raise serializers.ValidationError(
                {'retry error': 'This track on current Event already exist.'})

        return attrs


class EventSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    tracks = EventTrackSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'time_limit', 'max_tracks', 'author', 'tracks')


class EventTrackRatingSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = EventTrackRating
        fields = ('id', 'event_track', 'user', 'score',)
