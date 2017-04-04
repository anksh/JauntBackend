from django.db import models

# Create your models here.


class Jaunt(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    live = models.BooleanField()
    owner = models.IntegerField()
    title = models.CharField(max_length=256)
    shortcode = models.CharField(max_length=32)


class Membership(models.Model):
    user_id = models.IntegerField()
    jaunt = models.ForeignKey(Jaunt, on_delete=models.CASCADE)

