from django.db import models

# Create your models here.


class Jaunt(models.Model):
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    live = models.BooleanField(default=False)
    owner = models.CharField(max_length=64)
    title = models.CharField(max_length=256)
    shortcode = models.CharField(max_length=32)


class Membership(models.Model):
    user_id = models.CharField(max_length=64)
    jaunt = models.ForeignKey(Jaunt, on_delete=models.CASCADE)


class Photo(models.Model):
    id = models.IntegerField(primary_key=True)
    owner = models.CharField(max_length=64)
    original_url = models.CharField(max_length=512)
    thumbnail_url = models.CharField(max_length=512)
    taken_at = models.DateTimeField()
    jaunt = models.ForeignKey(Jaunt, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    deleted = models.BooleanField()
