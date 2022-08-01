from django.db import models

# Create your models here.
from Login.models import UserInfo


class TeamInfo(models.Model):
    teamID = models.AutoField(primary_key=True)
    teamname = models.CharField(max_length=128, unique=True)
    creator = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    createTime = models.DateTimeField(auto_now=True)


class TeamMember(models.Model):
    team = models.OneToOneField(TeamInfo, on_delete=models.CASCADE)
    member = models.OneToOneField(UserInfo, on_delete=models.CASCADE)


class Group(models.Model):
    groupId = models.AutoField(primary_key=True)
    groupName = models.CharField(max_length=100)
    creator = models.OneToOneField(UserInfo, on_delete=models.CASCADE, null=True)
    createdTime = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True)
    memberNum = models.IntegerField(default=0)



class GroupMember(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.OneToOneField(Group,on_delete=models.CASCADE)
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    joinTime = models.DateTimeField(null=True)
    isCreator = models.BooleanField(default=False)


class Document(models.Model):
    docId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    creator = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    created_time = models.DateTimeField(null=True)
    modified_time = models.DateTimeField(null=True)
    content = models.TextField(null=True)
    docRight = models.IntegerField(default=1)
    recycled = models.BooleanField(default=False)
    isOccupied = models.IntegerField(null=True)
    group = models.OneToOneField(Group,on_delete=models.CASCADE)

