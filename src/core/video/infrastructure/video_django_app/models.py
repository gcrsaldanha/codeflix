from uuid import uuid4

from django.db import models


class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    title = models.CharField(max_length=255)
    description = models.TextField()
    launch_year = models.IntegerField()  # changed from launched_at to launch_year
    duration = models.DecimalField(max_digits=10, decimal_places=2)
    opened = models.BooleanField()
    published = models.BooleanField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)

    categories = models.ManyToManyField('Category', related_name='videos')
    genres = models.ManyToManyField('Genre', related_name='videos')
    cast_members = models.ManyToManyField('CastMember', related_name='videos')

    banner = models.UUIDField(null=True, blank=True)
    thumbnail = models.UUIDField(null=True, blank=True)
    thumbnail_half = models.UUIDField(null=True, blank=True)
    trailer = models.UUIDField(null=True, blank=True)
    video = models.UUIDField(null=True, blank=True)

    # banner = models.OneToOneField('ImageMedia', null=True, blank=True, on_delete=models.SET_NULL)
    # thumbnail = models.OneToOneField('ImageMedia', null=True, blank=True, related_name='video_thumbnail', on_delete=models.SET_NULL)
    # thumbnail_half = models.OneToOneField('ImageMedia', null=True, blank=True, related_name='video_thumbnail_half', on_delete=models.SET_NULL)
    # trailer = models.OneToOneField('AudioVideoMedia', null=True, blank=True, related_name='video_trailer', on_delete=models.SET_NULL)
    # video = models.OneToOneField('AudioVideoMedia', null=True, blank=True, related_name='video_media', on_delete=models.SET_NULL)
