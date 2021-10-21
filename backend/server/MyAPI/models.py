from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Create your models here.
class Parameters(models.Model):
    inputFile = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='uploads', default='')
    paramList = models.TextField(max_length=256, default='')
    targetColumn = models.CharField(max_length=32, default='')
    adjust = models.FloatField(default=5.0)
    round = models.IntegerField(default=5)
    fixed = models.CharField(max_length=32, default='', blank=True)
    threshold = models.IntegerField(default=0)

    def __str__(self):
        return str(self.paramList)
