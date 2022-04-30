# Generated by Django 4.0.4 on 2022-04-30 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_log_reactions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='reactions',
        ),
        migrations.AddField(
            model_name='comment',
            name='reactions',
            field=models.CharField(blank=True, choices=[('thumb-up', 'U+1F44D'), ('heart-eyes', 'U+1F60D'), ('laughing-crying', 'U+1F602'), ('cowboy', 'U+1F920'), ('frown', 'U+2639'), ('angry', 'U+1F621')], max_length=20),
        ),
    ]
