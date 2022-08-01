from django.db import models

# Create your models here.
from TeamManager.models import Group
from Login.models import UserInfo


class ProjectInfo(models.Model):
    projectID = models.AutoField(primary_key=True)
    projectName = models.CharField(max_length=128, unique=True)
    projectTeam = models.OneToOneField(Group, on_delete=models.CASCADE)
    projectIntro = models.TextField
    projectStatus = models.BooleanField(default=False)  #False代表未被删除，True代表已经放入了回收站


class UMLInfo(models.Model):
    umlID = models.AutoField(primary_key=True)
    umlName = models.CharField(max_length=128, null=False)
    umlPath = models.CharField(max_length=200)
    umlCreator = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    umlCreateTime = models.DateTimeField(auto_now=True)
    umlProject = models.OneToOneField(ProjectInfo, on_delete=models.CASCADE)


class PageInfo(models.Model):
    pageID = models.AutoField(primary_key=True)
    pageName = models.CharField(max_length=128, null=False)
    pagePath = models.CharField(max_length=200)
    pageCreator = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    pageProject = models.OneToOneField(ProjectInfo, on_delete=models.CASCADE)
    pageCreateTime = models.DateTimeField(auto_now=True)


class PageEditor(models.Model):
    page = models.OneToOneField(PageInfo, on_delete=models.CASCADE)
    Editor = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
