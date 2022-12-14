from django.db import models

# Create your models here.
from TeamManager.models import Group
from Login.models import UserInfo


class ProjectInfo(models.Model):
    projectID = models.AutoField(primary_key=True)
    projectName = models.CharField(max_length=128)
    projectTeam = models.ForeignKey(Group, on_delete=models.CASCADE)
    projectIntro = models.CharField(max_length=100, null=True)
    projectStatus = models.BooleanField(default=False)  # False代表未被删除，True代表已经放入了回收站
    projectCreator = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    projectCreateTime = models.DateTimeField(auto_now=True)
    docNum = models.IntegerField(default=1)
    pageNum = models.IntegerField(default=0)
    copyNum = models.IntegerField(default=0)
    authority = models.BooleanField(default=False)  # False代表项目不开放预览 True代表开放预览权限


class UMLInfo(models.Model):
    umlID = models.AutoField(primary_key=True)
    umlName = models.CharField(max_length=128, null=False)
    umlPath = models.CharField(max_length=200, null=True)
    umlContent = models.TextField(null=True)
    umlCreator = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    umlCreateTime = models.DateTimeField(auto_now=True)
    umlProject = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)


class PageInfo(models.Model):
    pageID = models.AutoField(primary_key=True)
    pageName = models.CharField(max_length=128, null=False)
    # pagePath = models.CharField(max_length=200)
    pageContent = models.TextField(null=True)
    pageCreator = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    pageProject = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    pageCreateTime = models.DateTimeField(auto_now=True)


class PageEditor(models.Model):
    page = models.OneToOneField(PageInfo, on_delete=models.CASCADE)
    Editor = models.ForeignKey(UserInfo, on_delete=models.CASCADE)


class ProjectCollect(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    collectTime = models.DateTimeField(null=True)


class ProjectUser(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    lastWatch = models.DateTimeField(null=True)

    class Meta:
        ordering = ['-lastWatch']