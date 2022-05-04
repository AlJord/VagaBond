# Generated by Django 4.0.4 on 2022-05-04 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_merge_20220504_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='log',
        ),
        migrations.AddField(
            model_name='image',
            name='log_image',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='log', to='core.log'),
            preserve_default=False,
        ),
    ]
