from django.db import models

# Create your models here.
from Login.models import UserInfo


class TeamInfo(models.Model):
    teamID = models.AutoField(primary_key=True)
    teamname = models.CharField(max_length=128, unique=True)
    creator = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    createTime = models.DateTimeField(auto_now=True)
