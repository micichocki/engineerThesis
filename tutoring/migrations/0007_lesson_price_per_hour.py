# Generated by Django 5.1.3 on 2024-11-23 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0006_lesson_is_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='price_per_hour',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=4),
            preserve_default=False,
        ),
    ]
