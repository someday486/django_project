from django.db import models

# Create your models here.

class Destination(models.Model):
    id = models.IntegerField(null=False)
    palcename = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=15)   