# Generated by Django 5.1.3 on 2024-11-23 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0004_tutorprofile_isremote_user_city'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tutorprofile',
            old_name='isRemote',
            new_name='is_remote',
        ),
    ]