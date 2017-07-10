from django.db import models
import datetime
# Create your models here.


class Commodity(models.Model):
    name = models.CharField(max_length=2)
    price = models.FloatField()
    hour = models.CharField(max_length=2)
    minute = models.CharField(max_length=2)
    second = models.CharField(max_length=2)
    time = models.DateTimeField(auto_now_add=datetime.datetime.now().time())
    date = models.DateTimeField(auto_now_add=datetime.datetime.now())
    variation = models.CharField(max_length=20)
