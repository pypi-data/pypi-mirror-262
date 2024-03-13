# Generated by Django 3.1.13 on 2021-10-15 05:02

from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations


def modify_aa_team_token_add_page_ignore_paths(apps, schema_editor):
    # Add /admin/ and /user_notifications_count/ path to ignore

    AnalyticsPath = apps.get_model('analytics', 'AnalyticsPath')
    admin = AnalyticsPath.objects.create(ignore_path=r"^\/admin\/.*")
    user_notifications_count = AnalyticsPath.objects.create(ignore_path=r"^\/user_notifications_count\/.*")

    Tokens = apps.get_model('analytics', 'AnalyticsTokens')
    token = Tokens.objects.get(token="UA-186249766-2")
    token.ignore_paths.add(admin, user_notifications_count)


def undo_modify_aa_team_token_add_page_ignore_paths(apps, schema_editor):
    #
    AnalyticsPath = apps.get_model('analytics', 'AnalyticsPath')
    Tokens = apps.get_model('analytics', 'AnalyticsTokens')

    token = Tokens.objects.get(token="UA-186249766-2")
    try:
        admin = AnalyticsPath.objects.get(ignore_path=r"^\/admin\/.*", analyticstokens=token)
        user_notifications_count = AnalyticsPath.objects.get(ignore_path=r"^\/user_notifications_count\/.*", analyticstokens=token)
        admin.delete()
        user_notifications_count.delete()
    except ObjectDoesNotExist:
        # Its fine if it doesnt exist, we just dont want them building up when re-migrating
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_Generate_Identifier'),
    ]

    operations = [migrations.RunPython(modify_aa_team_token_add_page_ignore_paths, undo_modify_aa_team_token_add_page_ignore_paths)
    ]
