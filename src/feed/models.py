from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone

from user.models import User

# Create your models here.


class AcessPermissionChoices(models.IntegerChoices):
    PRIVATE = 0, '비공개'
    PUBLIC = 1, '전체 공개'
    FRIEND = 2, '친구 공개'


class Feed(models.Model):
    title = models.CharField('제목', max_length=100)
    thumbnail = models.CharField('썸네일', max_length=100)
    registration_date = models.DateTimeField('피드 등록일', default=timezone.now)
    contents = models.CharField('본문', max_length=2000)
    access_permission = models.SmallIntegerField('피드 접근 권한', default=AcessPermissionChoices.PUBLIC,
                                                 choices=AcessPermissionChoices.choices)
    user = models.ForeignKey(User, on_delete=CASCADE)
