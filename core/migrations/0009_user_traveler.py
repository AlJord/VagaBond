# Generated by Django 4.0.4 on 2022-04-26 15:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_trip_duration_log_date_logged_trip_begin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='traveler',
            field=models.ManyToManyField(related_name='travelers', to=settings.AUTH_USER_MODEL),
        ),
    ]