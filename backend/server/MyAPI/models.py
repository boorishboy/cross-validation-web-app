from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Create your models here.

class Parameters(models.Model):
    runid = models.AutoField(primary_key=True)
    upload_timestamp = models.DateTimeField(auto_now_add=True)
    file_hash = models.CharField(max_length=32, default=None)
    inputFile = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='uploads', default=None)
    paramList = models.TextField(default=None)
    targetColumn = models.CharField(max_length=64, default=None)
    adjust = models.FloatField(default=None, blank=True, null=True)
    round = models.IntegerField(default=5)
    fixed = models.CharField(max_length=32, default=None, blank=True, null=True)
    threshold = models.IntegerField(default=5, null=True, blank=True)

    def __str__(self):
        return str(self.upload_timestamp) + " " + str(self.paramList)

class Results(models.Model):
    runid = models.OneToOneField(
        Parameters,
        related_name = 'results',
        on_delete = models.CASCADE,
    )
    resultid = models.AutoField(primary_key=True)
    file_hash = models.CharField(max_length=64, default=None)
    upload_timestamp = models.DateTimeField(default=None)
    results_timestamp = models.DateTimeField(auto_now_add=True)
    rkf_scores = models.CharField(max_length=255, default=None)
    rkf_mean = models.FloatField(default=None)
    rkf_stddev = models.FloatField(default=None)
    cv_scores = models.CharField(max_length=255, default=None)
    cv_mean = models.FloatField(default=None)
    cv_stddev = models.FloatField(default=None)
    coefs_ols = models.TextField(default=None)
    coefs_nnls = models.TextField(default=None)
    outliers_ols = models.TextField(default=None)
    mean_abs_percentage_error_ols = models.FloatField(default=None)
    percentage_error_vect_ols = models.TextField(default=None)
    mean_percentage_error_ols = models.FloatField(default=None)
    median_percentage_error_ols = models.FloatField(default=None)
    rmsre_ols = models.FloatField(default=None)
    stddev_abs_percentage_error_ols = models.FloatField(default=None)
    stddev_relative_error_ols = models.FloatField(default=None)
    rmse_ols = models.FloatField(default=None)
    r2_score_ols = models.FloatField(default=None)
    outliers_nnls = models.TextField(default=None)
    mean_abs_percentage_error_nnls = models.FloatField(default=None)
    percentage_error_vect_nnls = models.TextField(default=None)
    mean_percentage_error_nnls = models.FloatField(default=None)
    median_percentage_error_nnls = models.FloatField(default=None)
    rmsre_nnls = models.FloatField(default=None)
    stddev_abs_percentage_error_nnls = models.FloatField(default=None)
    stddev_relative_error_nnls = models.FloatField(default=None)
    rmse_nnls = models.FloatField(default=None)
    r2_score_nnls = models.FloatField(default=None)
    y = models.TextField(default=None)



# class ResultsNNLS(models.Model):
#     runid = models.ForeignKey(
#         Parameters,
#         related_name = 'resultsnnls',
#         on_delete = models.CASCADE
#     )
#     resultnnlsid = models.AutoField(primary_key=True)
#     outliers = models.CharField(max_length=255, default=None)
#     mean_abs_percentage_error = models.FloatField(default=None)
#     percentage_error_vect = models.TextField(default=None)
#     mean_percentage_error = models.FloatField(default=None)
#     median_percentage_error = models.FloatField(default=None)
#     rmsre = models.FloatField(default=None)
#     stddev_abs_percentage_error = models.FloatField(default=None)
#     stddev_relative_error = models.FloatField(default=None)
#     rmse = models.CharField(max_length=64, default=None)
#     r2_score = models.CharField(max_length=64, default=None)
