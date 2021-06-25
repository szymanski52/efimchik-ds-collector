from django.db import models
from django.contrib.auth.models import User


class DataSet(models.Model):
    title = models.CharField(max_length=100, default='Efimchik Dataset')
    description = models.CharField(max_length=500, null=True)
    cover = models.ImageField(upload_to='ds_manager/static/covers', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    csv_file = models.FileField(upload_to='ds_manager/static/csvs', null=True)
    access = models.IntegerField(default=1)  # 0-private 1-public 2-community


class UserAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE)


class UserFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
