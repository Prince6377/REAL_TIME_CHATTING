# Generated by Django 5.1.3 on 2024-11-12 04:02

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rt_Chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmessages',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
        migrations.AlterField(
            model_name='groupname',
            name='group_name',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=100, unique=True),
        ),
    ]
