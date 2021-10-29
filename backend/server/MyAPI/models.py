from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Create your models here.
class Parameters(models.Model):
    inputFile = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='uploads', default=None)
    paramList = models.TextField(default=None, blank=True, null=True)
    targetColumn = models.CharField(max_length=64, default=None, null=True, blank=True)
    adjust = models.FloatField(default=None, blank=True, null=True)
    round = models.IntegerField(default=5)
    fixed = models.CharField(max_length=32, default=None, blank=True, null=True)
    threshold = models.IntegerField(default=5, null=True, blank=True)

    def __str__(self):
        return str(self.paramList)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

class ResultsOLS(models.Model):
    inputData = models.ForeignKey(
        Parameters,
        on_delete = models.CASCADE,
        null = True,
    )
    outliers = models.CharField(max_length=255, default=None, blank=True, null=True)
    mean_abs_percentage_error = models.FloatField(default=None, null=True, blank=True)
    percentage_error_vect = models.TextField(default=None, null=True, blank=True)
    mean_percentage_error = models.FloatField(default=None, null=True, blank=True)
    median_percentage_error = models.FloatField(default=None, null=True, blank=True)
    rmsre = models.FloatField(default=None, null=True, blank=True)
    stddev_abs_percentage_error = models.FloatField(default=None, null=True, blank=True)
    stddev_relative_error = models.FloatField(default=None, blank=True, null=True)
    rmse = models.CharField(max_length=64, default=None, blank=True, null=True)
    r2_score = models.CharField(max_length=64, default=None, null=True, blank=True)

class ResultsNNLS(models.Model):
    inputData = models.ForeignKey(
        Parameters,
        on_delete = models.CASCADE,
        null=True,
    )
    outliers = models.CharField(max_length=255, default=None, blank=True, null=True)
    mean_abs_percentage_error = models.FloatField(default=None, null=True, blank=True)
    percentage_error_vect = models.TextField(default=None, null=True, blank=True)
    mean_percentage_error = models.FloatField(default=None, null=True, blank=True)
    median_percentage_error = models.FloatField(default=None, null=True, blank=True)
    rmsre = models.FloatField(default=None, null=True, blank=True)
    stddev_abs_percentage_error = models.FloatField(default=None, null=True, blank=True)
    stddev_relative_error = models.FloatField(default=None, blank=True, null=True)
    rmse = models.CharField(max_length=64, default=None, blank=True, null=True)
    r2_score = models.CharField(max_length=64, default=None, null=True, blank=True)
