# Generated by Django 3.2 on 2022-08-05 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='realName',
            field=models.CharField(max_length=128),
        ),
    ]