# Generated by Django 4.0.4 on 2022-05-04 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_alter_image_log_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='log_image',
        ),
        migrations.AddField(
            model_name='image',
            name='log',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='log_image', to='core.log'),
            preserve_default=False,
        ),
    ]
