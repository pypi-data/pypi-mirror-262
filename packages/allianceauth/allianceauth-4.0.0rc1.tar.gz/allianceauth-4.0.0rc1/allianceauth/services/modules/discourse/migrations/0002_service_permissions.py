# Generated by Django 1.10.5 on 2017-02-02 05:59

from django.db import migrations
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.management import create_permissions

import logging

logger = logging.getLogger(__name__)


def migrate_service_enabled(apps, schema_editor):
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    DiscourseUser = apps.get_model("discourse", "DiscourseUser")

    perm = Permission.objects.get(codename='access_discourse')

    member_group_name = getattr(settings, 'DEFAULT_AUTH_GROUP', 'Member')
    blue_group_name = getattr(settings, 'DEFAULT_BLUE_GROUP', 'Blue')

    # Migrate members
    if DiscourseUser.objects.filter(user__groups__name=member_group_name).exists() or \
            getattr(settings, 'ENABLE_AUTH_DISCOURSE', False):
        try:
            group = Group.objects.get(name=member_group_name)
            group.permissions.add(perm)
        except ObjectDoesNotExist:
            logger.warning('Failed to migrate ENABLE_AUTH_DISCOURSE setting')

    # Migrate blues
    if DiscourseUser.objects.filter(user__groups__name=blue_group_name).exists() or \
            getattr(settings, 'ENABLE_BLUE_DISCOURSE', False):
        try:
            group = Group.objects.get(name=blue_group_name)
            group.permissions.add(perm)
        except ObjectDoesNotExist:
            logger.warning('Failed to migrate ENABLE_BLUE_DISCOURSE setting')



class Migration(migrations.Migration):

    dependencies = [
        ('discourse', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discourseuser',
            options={'permissions': (('access_discourse', 'Can access the Discourse service'),)},
        ),
        migrations.RunPython(migrate_service_enabled, migrations.RunPython.noop),
    ]
