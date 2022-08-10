from django.db import models

# Create your models here.
from Login.models import UserInfo
from ProjectManager.models import ProjectInfo
from TeamManager.models import Group


class Document(models.Model):
    docId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    created_time = models.DateTimeField(null=True)
    modified_time = models.DateTimeField(null=True)
    content = models.TextField(null=True)
    docRight = models.IntegerField(default=1)
    recycled = models.BooleanField(default=False)
    isOccupied = models.IntegerField(null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True)
    project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    type = models.BooleanField(default=False)#False表示文档是团队文档，True表示是项目文档
