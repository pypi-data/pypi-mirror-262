# Generated by Django 1.10.1 on 2016-09-09 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20160907_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='authservicesinfo',
            name='state',
            field=models.CharField(blank=True, choices=[(None, b'None'), (b'Blue', b'Blue'), (b'Member', b'Member')], default=None, max_length=10, null=True),
        ),
    ]
