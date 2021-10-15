from django.db import models

# Create your models here.
class parameters(models.Model):
    inputFile = models.FileField
    paramList = models.TextField
    targetColumn = models.CharField
    adjust = models.FloatField
    round = models.IntegerField
    fixed = models.CharField
