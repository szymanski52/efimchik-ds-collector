from django.db import models
from django.contrib.auth.models import User


class DataSet(models.Model):
    title = models.CharField(max_length=100, default='Dataset 1488')
    description = models.CharField(max_length=500, null=True)
    cover = models.ImageField(upload_to='covers', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    csv_file = models.FileField(upload_to='csvs', null=True)
