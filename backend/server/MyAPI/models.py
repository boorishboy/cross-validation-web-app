from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Create your models here.

class Parameters(models.Model):
    runid = models.AutoField(primary_key=True)
    inputFile = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='uploads', default=None)
    paramList = models.TextField(default=None)
    targetColumn = models.CharField(max_length=64, default=None)
    adjust = models.FloatField(default=None, blank=True, null=True)
    round = models.IntegerField(default=5)
    fixed = models.CharField(max_length=32, default=None, blank=True, null=True)
    threshold = models.IntegerField(default=5, null=True, blank=True)
    # resultsNNLS = models.ForeignKey(
    #     ResultsNNLS,
    #     on_delete=models.CASCADE
    #     )
    # resultsOLS = models.ForeignKey(
    #     ResultsOLS,
    #     on_delete=models.CASCADE
    #     )
    # class Meta:
    #         unique_together =(('resultsNNLS', 'resultsOLS'),)

    def __str__(self):
        return str(self.paramList)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


class ResultsOLS(models.Model):
    runid = models.ForeignKey(
        Parameters,
        related_name = 'resultsols',
        on_delete = models.CASCADE
    )
    resultolsid = models.AutoField(primary_key=True)
    outliers = models.CharField(max_length=255, default=None)
    mean_abs_percentage_error = models.FloatField(default=None)
    percentage_error_vect = models.TextField(default=None)
    mean_percentage_error = models.FloatField(default=None)
    median_percentage_error = models.FloatField(default=None)
    rmsre = models.FloatField(default=None)
    stddev_abs_percentage_error = models.FloatField(default=None)
    stddev_relative_error = models.FloatField(default=None)
    rmse = models.CharField(max_length=64, default=None)
    r2_score = models.CharField(max_length=64, default=None)


class ResultsNNLS(models.Model):
    runid = models.ForeignKey(
        Parameters,
        related_name = 'resultsnnls',
        on_delete = models.CASCADE
    )
    resultnnlsid = models.AutoField(primary_key=True)
    outliers = models.CharField(max_length=255, default=None)
    mean_abs_percentage_error = models.FloatField(default=None)
    percentage_error_vect = models.TextField(default=None)
    mean_percentage_error = models.FloatField(default=None)
    median_percentage_error = models.FloatField(default=None)
    rmsre = models.FloatField(default=None)
    stddev_abs_percentage_error = models.FloatField(default=None)
    stddev_relative_error = models.FloatField(default=None)
    rmse = models.CharField(max_length=64, default=None)
    r2_score = models.CharField(max_length=64, default=None)
