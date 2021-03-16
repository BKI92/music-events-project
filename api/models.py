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
    url = models.URLField('Ссылка на песню')

    class Meta:
        verbose_name = 'Трэк'
        verbose_name_plural = 'Трэки'

    def __str__(self):
        return f'{self.name} {self.artist}'


class EventTrack(models.Model):
    SCORES = zip(range(1, 11), range(1, 11))
    track = models.ForeignKey(Track,
                              on_delete=models.CASCADE,
                              related_name='event_track',
                              verbose_name='Трэк')

    user = models.ForeignKey(User,
                             on_delete=models.DO_NOTHING,
                             related_name='event_track',
                             verbose_name='Пользователь')
    score = models.IntegerField(choices=SCORES)

    class Meta:
        verbose_name = 'Трэк События'
        verbose_name_plural = 'Трэки События'

    def __str__(self):
        return f'{self.track}'
