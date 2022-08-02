from django.db import models

# Create your models here.
from Login.models import UserInfo


class Group(models.Model):
    groupId = models.AutoField(primary_key=True)
    groupName = models.CharField(max_length=100)
    creator = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=True)
    createdTime = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True)
    memberNum = models.IntegerField(default=1)


class GroupMember(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    joinTime = models.DateTimeField(auto_now_add=True)
    isCreator = models.BooleanField(default=False)
    isManager = models.BooleanField(default=False)

