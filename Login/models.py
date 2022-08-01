from django.db import models


# Create your models here.
class UserInfo(models.Model):
    userID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=128, unique=True)
    userpassword = models.CharField(max_length=128)
    useremail = models.EmailField(unique=True)
    realname = models.CharField(max_length=128, unique=True)