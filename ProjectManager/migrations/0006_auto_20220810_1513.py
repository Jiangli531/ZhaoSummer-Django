# Generated by Django 3.2 on 2022-08-10 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0002_alter_userinfo_realname'),
        ('ProjectManager', '0005_alter_projectinfo_projectname'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='umlinfo',
        #     name='umlPath',
        # ),
        migrations.AddField(
            model_name='projectinfo',
            name='copyNum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='umlinfo',
            name='umlContent',
            field=models.TextField(null=True),
        ),
        # migrations.CreateModel(
        #     name='ProjectUser',
        #     fields=[
        #         ('id', models.AutoField(primary_key=True, serialize=False)),
        #         ('lastWatch', models.DateTimeField(null=True)),
        #         ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProjectManager.projectinfo')),
        #         ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Login.userinfo')),
        #     ],
        #     options={
        #         'ordering': ['-lastWatch'],
        #     },
        # ),
        # migrations.CreateModel(
        #     name='ProjectCollect',
        #     fields=[
        #         ('id', models.AutoField(primary_key=True, serialize=False)),
        #         ('collectTime', models.DateTimeField(null=True)),
        #         ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProjectManager.projectinfo')),
        #         ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Login.userinfo')),
        #     ],
        # ),
    ]
