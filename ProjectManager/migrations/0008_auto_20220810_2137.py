# Generated by Django 3.2 on 2022-08-10 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0002_alter_userinfo_realname'),
        ('ProjectManager', '0007_umlinfo_umlpath'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectinfo',
            name='authority',
            field=models.BooleanField(default=False),
        ),
    ]
