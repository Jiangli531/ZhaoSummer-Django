# Generated by Django 3.2 on 2022-08-02 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ProjectManager', '0001_initial'),
        ('TeamManager', '0002_auto_20220802_1539'),
        ('Login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectinfo',
            name='projectTeam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TeamManager.group'),
        ),
        migrations.AddField(
            model_name='pageinfo',
            name='pageCreator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Login.userinfo'),
        ),
        migrations.AddField(
            model_name='pageinfo',
            name='pageProject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProjectManager.projectinfo'),
        ),
        migrations.AddField(
            model_name='pageeditor',
            name='Editor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Login.userinfo'),
        ),
        migrations.AddField(
            model_name='pageeditor',
            name='page',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ProjectManager.pageinfo'),
        ),
    ]
