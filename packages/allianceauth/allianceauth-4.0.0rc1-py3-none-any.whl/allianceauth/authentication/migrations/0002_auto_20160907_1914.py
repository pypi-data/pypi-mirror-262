# Generated by Django 1.10.1 on 2016-09-07 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authservicesinfo',
            name='pathfinder_password',
        ),
        migrations.RemoveField(
            model_name='authservicesinfo',
            name='pathfinder_username',
        ),
    ]
