from django.db import models


# Create your models here.
class UserInfo(models.Model):
    userID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=128, unique=True)
    userpassword = models.CharField(max_length=128)
    useremail = models.EmailField(unique=True)
    realName = models.CharField(max_length=128, unique=True)
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name



class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('UserInfo', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ": " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = verbose_name