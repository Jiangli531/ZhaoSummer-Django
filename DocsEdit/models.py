from django.db import models

# Create your models here.
from Login.models import UserInfo
from TeamManager.models import TeamInfo


class DocsInfo(models.Model):
        docsID = models.AutoField(primary_key=True)
        docsTitle = models.CharField(max_length=128, unique=True)
        docsCreator = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
        createTime = models.DateTimeField(auto_now=True)
        editTime = models.DateTimeField(auto_now=True)
        content = models.TextField
        docsTeam = models.OneToOneField(TeamInfo, on_delete=models.CASCADE)
        docsStatus = models.BooleanField(default=False)  #False代表未被删除，True代表已经放入了回收站