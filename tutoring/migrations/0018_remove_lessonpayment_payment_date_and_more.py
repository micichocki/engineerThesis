# Generated by Django 5.1.3 on 2024-12-06 22:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0017_remove_lessonpayment_payment_lessonpayment_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessonpayment',
            name='payment_date',
        ),
        migrations.AddField(
            model_name='lessonpayment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
