from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from api.models import Event, EventTrack, EventTrackRating, Track
from music_events import settings

END_TIME = '2025-04-23T14:04:52.045283+03:00'
User = get_user_model()


class ApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="sarah", email="connor.s@skynet.com",
            password="12345qwerty"
        )

        self.client.force_authenticate(user=self.user)
        self.event = Event.objects.create(title='Test1',
                                          time_limit=END_TIME,
                                          author=self.user,
                                          max_tracks=10)
        self.track = Track.objects.create(name='Believer',
                                          artist='Imagine Dragons',
                                          url='https://www.last.fm/music/'
                                              'Imagine+Dragons/')

    @override_settings(CACHES=settings.TEST_CACHES)
    def test_tracks_list(self):
        """Тест успешного получения списка трэков с last.fm"""

        name = 'Du hust'
        response = self.client.get('/api/v1/tracks/', {'name': name})
        self.assertEqual(response.status_code, 200,
                         'Ожидается статус код 200')

    @override_settings(CACHES=settings.TEST_CACHES)
    def test_post_track(self):
        """Тест добавления трэка в базу."""

        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Fire',
            'temp_id': '0'
        }
        response = self.client.post('/api/v1/tracks/', data)
        added_track = Track.objects.get(name='Fire')
        self.assertEqual(response.status_code, 200,
                         'Ожидается статус код 200')
        self.assertEqual(added_track.name, 'Fire',
                         'Не получилось записать данный трэк в базу')

    @override_settings(CACHES=settings.TEST_CACHES)
    def test_loaded_tracks(self):
        """Тест получения списка добавленных трэков"""

        response = self.client.get('/api/v1/tracks/loaded/', format='json')
        name = response.data.get('results')[0].get('name')
        artist = response.data.get('results')[0].get('artist')
        self.assertEqual([name, artist], ['Believer', 'Imagine Dragons'])

    def test_list_events(self):
        """Тест получения списка событий"""

        response = self.client.get('/api/v1/events/', format='json')
        title = response.data.get('results')[0].get('title')
        time_limit = response.data.get('results')[0].get('time_limit')
        author = response.data.get('results')[0].get('author')
        max_tracks = response.data.get('results')[0].get('max_tracks')
        self.assertEqual([title, time_limit, author, max_tracks],
                         ['Test1', END_TIME, 'sarah', 10])

    def test_post_events(self):
        """Тест  создания события"""
        data = {
            'title': 'Test Event',
            'time_limit': END_TIME,
            'author': self.user,
            'max_tracks': 10
        }
        self.client.post('/api/v1/events/', data)
        added_event = Event.objects.get(title='Test Event')
        self.assertEqual(added_event.title, 'Test Event',
                         'Не получилось создать событие')

    def test_post_events_false(self):
        """Тест   успешного добавления трэка к событию"""
        data = {
            'time_limit': END_TIME,
            'author': self.user,
            'max_tracks': 10
        }
        self.client.post('/api/v1/events/', data)
        added_event = Event.objects.filter(title='Test Event')
        self.assertNotEqual(added_event, None)

    def test_add_track_to_event_false(self):
        """Тест  попытки добавления уже добавленного трэка к событию"""
        data = {
            'event': self.event.id,
            'track': self.track.id
        }

        self.client.post('/api/v1/events/tracks/', data)
        self.client.post('/api/v1/events/tracks/', data)

        amount = EventTrack.objects.all().count()
        self.assertEqual(amount, 1)

    def test_list_events_tracks(self):
        """Тест получения списка треков события"""
        EventTrack.objects.create(event=self.event, track=self.track)
        self.client.get('/api/v1/events/tracks/')
        amount = EventTrack.objects.all().count()
        self.assertEqual(amount, 1)

    def test_add_rating(self):
        """Тест оценки трэка события."""

        event_track = EventTrack.objects.create(event=self.event,
                                                track=self.track)
        data = {
            'event_track': event_track.id,
            'score': 8,
            'user': self.user.id
        }
        self.client.post('/api/v1/ratings/', data)
        score = EventTrackRating.objects.get(event_track=event_track.id,
                                             user=self.user.id).score

        self.assertEqual(score, 8)

    def test_add_rating_unique(self):
        """Тест невозможности повторноой оценки  трэка к событию """

        event_track = EventTrack.objects.create(event=self.event,
                                                track=self.track)
        data = {
            'event_track': event_track.id,
            'score': 8,
            'user': self.user.id
        }
        data2 = {
            'event_track': event_track.id,
            'score': 10,
            'user': self.user.id
        }
        self.client.post('/api/v1/ratings/', data)
        self.client.post('/api/v1/ratings/', data2)

        amount = EventTrackRating.objects.filter(
            event_track=event_track.id).count()

        self.assertEqual(amount, 1)
