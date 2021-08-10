from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone

from user.models import User

# Create your models here.


class Feed(models.Model):
    title = models.CharField(max_length=100)
    thumbnail = models.CharField(max_length=100)
    registration_date = models.DateTimeField(default=timezone.now)
    contents = models.CharField(max_length=2000)
    is_show = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=CASCADE)
