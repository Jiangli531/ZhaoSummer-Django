from django.db import models

# Create your models here.

class TeamInfo(models.Model):
    teamID = models.AutoField(primary_key=True)
    teamname = models.CharField(max_length=128, unique=True)
    creater = models.OneToOneField('UserInfo', on_delete=models.CASCADE)
    createtime = models.DateTimeField(auto_now=True)
