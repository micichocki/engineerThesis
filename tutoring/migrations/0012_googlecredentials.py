# Generated by Django 5.1.3 on 2024-11-30 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0011_lesson_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleCredentials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField()),
                ('refresh_token', models.TextField()),
                ('token_uri', models.TextField()),
                ('client_id', models.TextField()),
                ('client_secret', models.TextField()),
                ('scopes', models.TextField()),
            ],
        ),
    ]
