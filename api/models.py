from django.db import models

# Create your models here.

class Jaunt(models.Model):
    start = models.DateTimeField()