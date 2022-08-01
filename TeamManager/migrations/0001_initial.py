# Generated by Django 3.2 on 2022-08-01 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamInfo',
            fields=[
                ('teamID', models.AutoField(primary_key=True, serialize=False)),
                ('teamname', models.CharField(max_length=128, unique=True)),
                ('createTime', models.DateTimeField(auto_now=True)),
                ('creator', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Login.userinfo')),
            ],
        ),
    ]
