# Generated by Django 3.2.8 on 2021-12-27 16:04

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parameters',
            fields=[
                ('runid', models.AutoField(primary_key=True, serialize=False)),
                ('upload_timestamp', models.DateTimeField(default=None)),
                ('file_hash', models.CharField(default=None, max_length=32)),
                ('inputFile', models.FileField(default=None, storage=django.core.files.storage.FileSystemStorage(location='/Users/boorish/Documents/programowanie/engineer/code/cross-validation-web-app/backend/server/media'), upload_to='uploads')),
                ('paramList', models.TextField(default=None)),
                ('targetColumn', models.CharField(default=None, max_length=64)),
                ('adjust', models.FloatField(blank=True, default=None, null=True)),
                ('round', models.IntegerField(default=5)),
                ('fixed', models.CharField(blank=True, default=None, max_length=32, null=True)),
                ('threshold', models.IntegerField(blank=True, default=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('resultid', models.AutoField(primary_key=True, serialize=False)),
                ('file_hash', models.CharField(default=None, max_length=64)),
                ('upload_timestamp', models.DateTimeField(default=None)),
                ('results_timestamp', models.DateTimeField(default=None)),
                ('rkf_scores', models.CharField(default=None, max_length=255)),
                ('rkf_mean', models.FloatField(default=None)),
                ('rkf_stddev', models.FloatField(default=None)),
                ('cv_scores', models.CharField(default=None, max_length=255)),
                ('cv_mean', models.FloatField(default=None)),
                ('cv_stddev', models.FloatField(default=None)),
                ('coefs_ols', models.TextField(default=None)),
                ('coefs_nnls', models.TextField(default=None)),
                ('outliers_ols', models.TextField(default=None)),
                ('mean_abs_percentage_error_ols', models.FloatField(default=None)),
                ('percentage_error_vect_ols', models.TextField(default=None)),
                ('mean_percentage_error_ols', models.FloatField(default=None)),
                ('median_percentage_error_ols', models.FloatField(default=None)),
                ('rmsre_ols', models.FloatField(default=None)),
                ('stddev_abs_percentage_error_ols', models.FloatField(default=None)),
                ('stddev_relative_error_ols', models.FloatField(default=None)),
                ('rmse_ols', models.FloatField(default=None)),
                ('r2_score_ols', models.FloatField(default=None)),
                ('outliers_nnls', models.TextField(default=None)),
                ('mean_abs_percentage_error_nnls', models.FloatField(default=None)),
                ('percentage_error_vect_nnls', models.TextField(default=None)),
                ('mean_percentage_error_nnls', models.FloatField(default=None)),
                ('median_percentage_error_nnls', models.FloatField(default=None)),
                ('rmsre_nnls', models.FloatField(default=None)),
                ('stddev_abs_percentage_error_nnls', models.FloatField(default=None)),
                ('stddev_relative_error_nnls', models.FloatField(default=None)),
                ('rmse_nnls', models.FloatField(default=None)),
                ('r2_score_nnls', models.FloatField(default=None)),
                ('y', models.TextField(default=None)),
                ('runid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='MyAPI.parameters')),
            ],
        ),
    ]
