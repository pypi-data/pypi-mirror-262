# Generated by Django 1.10.2 on 2016-12-04 10:25

from django.conf import settings
from django.db import migrations, models
from django.core.exceptions import ObjectDoesNotExist
import django.db.models.deletion


def internal_group(group):
    return (
        "Corp_" in group.name or
        "Alliance_" in group.name or
        settings.DEFAULT_AUTH_GROUP in group.name or
        settings.DEFAULT_BLUE_GROUP in group.name
    )


def combine_group_models(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    AuthGroup = apps.get_model("groupmanagement", "AuthGroup")

    for group in Group.objects.all():
        authgroup = AuthGroup(group=group)
        if not hasattr(group, 'hiddengroup'):
            authgroup.hidden = False
        if hasattr(group, 'opengroup'):
            authgroup.open = True

        if hasattr(group, 'groupdescription'):
            authgroup.description = group.groupdescription.description

        authgroup.internal = internal_group(group)
        authgroup.save()


def reverse_group_models(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    GroupDescription = apps.get_model("groupmanagement", "GroupDescription")
    OpenGroup = apps.get_model("groupmanagement", "OpenGroup")
    HiddenGroup = apps.get_model("groupmanagement", "HiddenGroup")

    for group in Group.objects.all():
        if not hasattr(group, 'authgroup') or group.authgroup is None:
            continue
        if group.authgroup.open:
            OpenGroup.objects.get_or_create(group=group)
        else:
            try:
                OpenGroup.objects.get(group=group).delete()
            except ObjectDoesNotExist:
                pass

        if group.authgroup.hidden:
            HiddenGroup.objects.get_or_create(group=group)
        else:
            try:
                HiddenGroup.objects.get(group=group).delete()
            except ObjectDoesNotExist:
                pass

        if len(group.authgroup.description):
            GroupDescription.objects.update_or_create(group=group, defaults={'description': group.authgroup.description})


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groupmanagement', '0003_default_groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.Group')),
                ('internal', models.BooleanField(default=True, help_text='Internal group, users cannot see, join or request to join this group.<br>Used for groups such as Members, Corp_*, Alliance_* etc.<br><b>Overrides Hidden and Open options when selected.</b>')),
                ('hidden', models.BooleanField(default=True, help_text='Group is hidden from users but can still join with the correct link.')),
                ('open', models.BooleanField(default=False, help_text='Group is open and users will be automatically added upon request. <br>If the group is not open users will need their request manually approved.')),
                ('description', models.CharField(max_length=512, blank=True, help_text='Description of the group shown to users.', )),

                ('group_leaders', models.ManyToManyField(related_name='leads_groups', to=settings.AUTH_USER_MODEL, blank=True, help_text='Group leaders can process group requests for this group specifically. Use the auth.group_management permission to allow a user to manage all groups.',)),
            ],
        ),
        migrations.RunPython(combine_group_models, reverse_group_models),
        migrations.RemoveField(
            model_name='groupdescription',
            name='group',
        ),
        migrations.RemoveField(
            model_name='hiddengroup',
            name='group',
        ),
        migrations.RemoveField(
            model_name='opengroup',
            name='group',
        ),
        migrations.DeleteModel(
            name='GroupDescription',
        ),
        migrations.DeleteModel(
            name='HiddenGroup',
        ),
        migrations.DeleteModel(
            name='OpenGroup',
        ),
    ]
