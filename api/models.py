from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Event(models.Model):
    title = models.CharField('Название события', unique=True, max_length=100)
    time_limit = models.DateTimeField('Ограничение времени')
    author = models.ForeignKey(User,
                               on_delete=models.PROTECT,
                               related_name='event',
                               verbose_name='Автор')
    tracks = models.ManyToManyField('EventTrack',
                                    verbose_name='Трэки',
                                    related_name='event_tracks')
    max_tracks = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return f'{self.title}'


class Track(models.Model):
    name = models.CharField('Название', max_length=100)
    artist = models.CharField('Артист', max_length=100)
    url = models.URLField('Ссылка на песню', unique=True)

    class Meta:
        verbose_name = 'Трэк'
        verbose_name_plural = 'Трэки'

    def __str__(self):
        return f'{self.name} {self.artist}'


class EventTrack(models.Model):
    event = models.ForeignKey(Event,
                              on_delete=models.CASCADE,
                              related_name='event_track',
                              verbose_name='Событие')
    track = models.ForeignKey(Track,
                              on_delete=models.CASCADE,
                              related_name='event_track',
                              verbose_name='Трэк')

    class Meta:
        verbose_name = 'Трэк События'
        verbose_name_plural = 'Трэки События'

    def __str__(self):
        return f'{self.track}'


class EventTrackRating(models.Model):
    SCORES = zip(range(1, 11), range(1, 11))

    event_track = models.ForeignKey(EventTrack,
                                    on_delete=models.CASCADE,
                                    related_name='event_track_rating',
                                    verbose_name='Трэк')

    user = models.ForeignKey(User,
                             on_delete=models.DO_NOTHING,
                             related_name='rating',
                             verbose_name='Пользователь')
    score = models.IntegerField(choices=SCORES, default=10)

    class Meta:
        verbose_name = 'Рэйтинг'
        verbose_name_plural = 'Рэйтинги'

    def __str__(self):
        return f'{self.user}:{self.event_track} - {self.score}'
